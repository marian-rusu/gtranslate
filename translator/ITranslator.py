import abc
from typing import Optional


class ITranslator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def translate(self, text: str, lang_tgt: str, lang_src: str) -> Optional[str]:
        pass
