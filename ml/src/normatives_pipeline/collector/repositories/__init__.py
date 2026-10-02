"""Слой repositories: доступ к данным реестров."""

from .faufcc import FaufccRepository
from .fgiscs import FgiscsRepository
from .pravo import PravoRepository

__all__ = ["FaufccRepository", "FgiscsRepository", "PravoRepository"]
