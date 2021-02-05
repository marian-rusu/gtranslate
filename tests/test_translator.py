from translator import translator
from unittest.mock import Mock, call

import unittest


class TestTranslator(unittest.TestCase):
    def setUp(self) -> None:
        self._g_translator = Mock()
        self._g_translator.translate.return_value = 'translated sentence'
        self._translator = translator.Translator(translator=self._g_translator)

    def test_translator_pass(self):
        res = self._translator.translate(
            sentence="test sentence", lang_tgt='en')
        self.assertEqual('translated sentence', res)
        self.assertEqual(
            call(text='test sentence', lang_tgt='en', lang_src='auto'),
            self._g_translator.translate.call_args)

    def test_traslator_wrong_language(self):
        res = self._translator.translate(
            sentence="test sentence", lang_tgt='gr')
        self.assertIsNone(res)
        self.assertFalse(self._g_translator.called)
