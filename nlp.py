"""Componentes pequenos de NLP para preparar texto antes de clasificar."""

import re
import unicodedata


class TextPreprocessor:
    """Normaliza acentos, puntuacion y stopwords en espanol e ingles."""

    STOPWORDS = frozenset(
        {
            "el",
            "la",
            "los",
            "las",
            "un",
            "una",
            "unos",
            "unas",
            "de",
            "del",
            "a",
            "ante",
            "con",
            "en",
            "para",
            "por",
            "que",
            "es",
            "son",
            "y",
            "o",
            "the",
            "an",
            "of",
            "in",
            "to",
            "for",
        }
    )

    def normalize(self, text: str | None) -> str:
        if not text:
            return ""

        without_accents = "".join(
            character
            for character in unicodedata.normalize("NFD", text)
            if unicodedata.category(character) != "Mn"
        )
        clean_text = re.sub(r"[^a-zA-Z0-9\\s]", " ", without_accents.lower())
        return " ".join(
            token for token in clean_text.split() if token not in self.STOPWORDS
        )
