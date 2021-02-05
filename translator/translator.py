import logging
from typing import Optional

from translator.g_translator import ITranslator


logger = logging.getLogger(__name__)


class Translator:
    accepted_languages = ["en", "it", "de"]

    def __init__(self, translator: ITranslator) -> None:
        self._translator = translator

    def translate(self, sentence: str, lang_tgt: str = 'en') -> Optional[str]:
        """Translate a sentence to a certain language. Google language detection is used as source language."""
        if lang_tgt not in self.accepted_languages:
            logger.info(f"Selected language {lang_tgt} not allowed! Available languages: {self.accepted_languages}")
            return None

        result = self._translator.translate(text=sentence, lang_tgt=lang_tgt, lang_src='auto')
        if result is None:
            logger.info(f"Sentence {sentence} can not be translated in: {lang_tgt}!")
        return result
