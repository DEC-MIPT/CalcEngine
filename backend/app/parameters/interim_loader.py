import logging
from collections.abc import Collection
from dataclasses import dataclass
from pathlib import Path

import yaml
from pydantic import BaseModel, ValidationError

from app.core.exceptions import ParameterValidationError
from app.parameters.interim_schemas import InterimManifest, InterimTypeFile, problems

logger = logging.getLogger("app.parameters.interim_loader")

MANIFEST = "manifest.yaml"
SUFFIX = ".yaml"


@dataclass(frozen=True)
class InterimFile:
    """Проверенный файл типа расчёта.

    Attributes:
        path: путь файла от корня данных, например ``<document>/<type>.yaml``.
        calculation_type: тип расчёта, имя файла без расширения.
        content: содержимое файла.
    """

    path: str
    calculation_type: str
    content: InterimTypeFile


@dataclass(frozen=True)
class InterimDocument:
    """Проверенный каталог документа нормы (``interim-normatives-source`` design.md, решение 1).

    Attributes:
        name: имя каталога документа.
        manifest: манифест документа.
        files: файлы типов в порядке их путей, в том числе файлы незарегистрированных типов.
    """

    name: str
    manifest: InterimManifest
    files: tuple[InterimFile, ...]


def _read(path: Path, shown: str) -> object:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        mark = getattr(error, "problem_mark", None)
        where = "" if mark is None else f" at line {mark.line + 1}"
        raise ParameterValidationError(f"{shown}: not valid YAML{where}") from None


def _validated[ModelT: BaseModel](model: type[ModelT], data: object, shown: str) -> ModelT:
    try:
        return model.model_validate(data)
    except ValidationError as error:
        raise ParameterValidationError(f"{shown}: {'; '.join(problems(error))}") from None


def _readable(entry: Path, root: Path) -> bool:
    """Читается ли файл каталога документа; пропущенный называет одна строка лога.

    Ссылка, которая ведёт за корень данных, и всё, что не файл ``.yaml``, не читаются
    (``interim-normatives`` "Non-functional — interim source").
    """
    shown = entry.relative_to(root).as_posix()
    target = entry.resolve()
    if not target.is_relative_to(root):
        logger.warning("code=interim_file_skipped file=%s reason=link_outside_root", shown)
        return False
    if not target.is_file() or entry.suffix != SUFFIX:
        logger.warning("code=interim_file_skipped file=%s reason=not_a_data_file", shown)
        return False
    return True


def _check_verifiers(content: InterimTypeFile, manifest: InterimManifest, shown: str) -> None:
    for path, record in content.records():
        verification = record.verification
        if verification.status != "pending" and verification.by not in manifest.verifiers:
            raise ParameterValidationError(f"{shown}: {path}.verification.by: not a listed verifier")


def _document(directory: Path, root: Path, registered: Collection[str]) -> InterimDocument:
    name = directory.name
    entries = [entry for entry in sorted(directory.iterdir()) if _readable(entry, root)]
    manifest_path = directory / MANIFEST
    if manifest_path not in entries:
        raise ParameterValidationError(f"{name}: no {MANIFEST}")
    manifest = _validated(InterimManifest, _read(manifest_path, f"{name}/{MANIFEST}"), f"{name}/{MANIFEST}")
    files: list[InterimFile] = []
    for entry in entries:
        if entry == manifest_path:
            continue
        shown = f"{name}/{entry.name}"
        content = _validated(InterimTypeFile, _read(entry, shown), shown)
        _check_verifiers(content, manifest, shown)
        if entry.stem not in registered:
            logger.warning("code=interim_type_unregistered file=%s", shown)
        files.append(InterimFile(path=shown, calculation_type=entry.stem, content=content))
    return InterimDocument(name=name, manifest=manifest, files=tuple(files))


def load_interim_root(root: Path, registered: Collection[str]) -> tuple[InterimDocument, ...]:
    """Читает и проверяет каталог временных нормативных данных (design.md, решения 1-3, 5).

    Корень разрешается один раз. Читаются только ``manifest.yaml`` и ``<type>.yaml`` прямо
    в каталоге документа, ``yaml.safe_load``; ссылка за корень и любой другой файл
    пропускаются с одной строкой лога. Файл незарегистрированного типа проверяется и
    остаётся в документе, а строка лога называет его. В лог и в ошибки значения данных не
    попадают.

    Args:
        root: корень данных.
        registered: зарегистрированные типы расчёта.

    Returns:
        Документы в порядке имён их каталогов.

    Raises:
        ParameterValidationError: если корня нет, у документа нет манифеста, файл не YAML
            или не проходит схему, ``by`` проверенной записи не назван в ``verifiers`` или у
            одного типа файлы в двух документах. Сообщение называет файл и путь поля.
    """
    resolved = root.resolve()
    if not resolved.is_dir():
        raise ParameterValidationError(f"the interim data root {resolved} is not a directory")
    documents: list[InterimDocument] = []
    for entry in sorted(resolved.iterdir()):
        target = entry.resolve()
        if not target.is_relative_to(resolved) or not target.is_dir():
            reason = "link_outside_root" if not target.is_relative_to(resolved) else "not_a_document_directory"
            logger.warning("code=interim_file_skipped file=%s reason=%s", entry.name, reason)
            continue
        documents.append(_document(entry, resolved, registered))
    owners: dict[str, str] = {}
    for document in documents:
        for found in document.files:
            if found.calculation_type in owners:
                raise ParameterValidationError(
                    f"{found.path}: the type also has data in {owners[found.calculation_type]}"
                )
            owners[found.calculation_type] = found.path
    return tuple(documents)
