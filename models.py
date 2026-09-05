"""Modelos de dominio usados por el clasificador."""

from dataclasses import dataclass
from enum import Enum


class CloudModel(str, Enum):
    """Modelos de servicio cloud soportados por la aplicacion."""

    IAAS = "IaaS"
    PAAS = "PaaS"
    SAAS = "SaaS"
    FAAS = "FaaS"


@dataclass(frozen=True)
class ClassificationResult:
    """Resultado completo de una clasificacion, listo para UI o CLI."""

    model: CloudModel | None
    scores: dict[CloudModel, int]
    normalized_text: str
    message: str

    @property
    def is_success(self) -> bool:
        return self.model is not None
