"""Reglas de dominio para clasificar servicios cloud."""

import re
from collections.abc import Iterable

from models import ClassificationResult, CloudModel
from nlp import TextPreprocessor


class CloudServiceClassifier:
    """Clasifica descripciones cloud mediante palabras y expresiones clave."""

    KEYWORDS: dict[CloudModel, tuple[str, ...]] = {  # noqa: RUF012
        CloudModel.IAAS: (
            r"vm",
            r"virtual machine",
            r"servidor(?:es)?",
            r"server(?:s)?",
            r"storage(?:s)?",
            r"red(?:es)?",
            r"network(?:s)?",
            r"subnet(?:s)?",
            r"vpc",
            r"vpn",
            r"balanceador(?:es)?",
            r"load balancer(?:s)?",
            r"infraestructura(?:s)?",
            r"infrastructure(?:s)?",
        ),
        CloudModel.PAAS: (
            r"plataforma(?:s)?",
            r"platform(?:s)?",
            r"runtime(?:s)?",
            r"framework(?:s)?",
            r"desplegar",
            r"deploy",
            r"despliegue(?:s)?",
            r"hosting",
            r"hosteo",
            r"app service(?:s)?",
            r"base de datos administrada(?:s)?",
            r"managed database(?:s)?",
            r"contenedor(?:es)? administrado(?:s)?",
            r"ci/cd",
            r"aplicacion(?:es)? web",
            r"web app",
            r"servidores gestionados",
        ),
        CloudModel.SAAS: (
            r"aplicacion(?:es)? lista(?:s)?",
            r"software as a service",
            r"crm",
            r"email",
            r"correo(?:s)?",
            r"office",
            r"google workspace",
            r"sistema en linea(?:s)?",
            r"suscripcion(?:es)?",
            r"software(?:s)?",
        ),
        CloudModel.FAAS: (
            r"funcion(?:es)?",
            r"function(?:s)?",
            r"serverless",
            r"evento(?:s)?",
            r"event-driven",
            r"lambda(?:s)?",
            r"trigger(?:s)?",
            r"disparador(?:es)?",
            r"ejecucion(?:es)? bajo demanda",
            r"on demand",
        ),
    }

    def __init__(self, preprocessor: TextPreprocessor | None = None) -> None:
        self.preprocessor = preprocessor or TextPreprocessor()
        self._patterns = {
            model: tuple(re.compile(rf"\b(?:{keyword})\b") for keyword in keywords)
            for model, keywords in self.KEYWORDS.items()
        }

    def classify(self, text: str | None) -> ClassificationResult:
        normalized_text = self.preprocessor.normalize(text)
        empty_scores = {model: 0 for model in CloudModel}

        if not normalized_text:
            return ClassificationResult(
                None,
                empty_scores,
                normalized_text,
                "Ingresa una descripcion para clasificarla.",
            )
        if len(normalized_text) < 3:
            return ClassificationResult(
                None,
                empty_scores,
                normalized_text,
                "La descripcion es demasiado corta para ser clasificada.",
            )

        scores = {
            model: self._count_matches(patterns, normalized_text)
            for model, patterns in self._patterns.items()
        }
        best_model = max(scores, key=scores.get)
        best_score = scores[best_model]
        if best_score == 0:
            return ClassificationResult(
                None,
                scores,
                normalized_text,
                "No se pudo determinar un modelo Cloud principal con las reglas actuales.",
            )

        return ClassificationResult(
            best_model,
            scores,
            normalized_text,
            f"Modelo principal: {best_model.value} (coincidencias: {best_score})",
        )

    @staticmethod
    def _count_matches(patterns: Iterable[re.Pattern[str]], text: str) -> int:
        return sum(len(pattern.findall(text)) for pattern in patterns)


if __name__ == "__main__":
    from cli import main

    raise SystemExit(main())
