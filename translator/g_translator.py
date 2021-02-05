import logging
from typing import Optional

from google_trans_new import google_translator

from translator.ITranslator import ITranslator

LOGGER = logging.getLogger(__name__)


class GTranslator(ITranslator):
    def __init__(self):
        self._translator = google_translator()

    def translate(self, text: str, lang_tgt: str = 'en', lang_src: str = 'auto') -> Optional[str]:
        """Implementation for translate function using google_trans_new."""
        result = None
        try:
            result = self._translator.translate(text, lang_tgt, lang_src)
        except Exception as exception:
            LOGGER.exception(f"Got exception in GTranslator: {exception}!")
        return result
