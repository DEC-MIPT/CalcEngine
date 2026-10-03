from pydantic import BaseModel, ConfigDict


class EngineerRule(BaseModel):
    """Правило, которое инженер-проектировщик задаёт там, где норма его не даёт.

    Допускается только как источник правила округления или проверенного диапазона
    (`calculation-core-contract` design.md, `NormRef`, резолюция 3); движок сам
    такое правило не выбирает. Оба поля обязательны: в конверте и отчёте правило
    видно как заданное инженером, а не молча принятое.
    """

    model_config = ConfigDict(extra="forbid")

    engineer: str
    rationale: str
