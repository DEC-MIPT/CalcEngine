from pydantic import BaseModel, ConfigDict, Field


class EngineerRule(BaseModel):
    """Правило, которое инженер-проектировщик задаёт там, где норма его не даёт.

    Допускается только как источник правила округления или проверенного диапазона
    (`calculation-core-contract` design.md, `NormRef`, резолюция 3); движок сам
    такое правило не выбирает. Оба поля обязательны и не пусты (хотя бы один
    непробельный символ): в конверте и отчёте правило видно как заданное инженером, а
    не молча принятое. Модель неизменяема, как и остальные межслойные типы.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    engineer: str = Field(pattern=r"\S")
    rationale: str = Field(pattern=r"\S")
