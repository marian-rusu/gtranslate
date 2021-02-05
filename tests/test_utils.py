import time
from multiprocessing import Lock

from pathlib import Path

import unittest

from translator import utils


class UtilsTests(unittest.TestCase):

    def test_extract_sentences_nominal(self) -> None:
        input_file_path = Path('input_file.txt')
        sentences = utils.extract_sentences(input_file_path)
        self.assertEqual(['sentence1', 'sentence2', 'sentence3',
                          'sentence4', 'sentence5            sentence5'],
                         sentences)

    def test_extract_sentences_invalid_path(self) -> None:
        input_file_path = Path('invalid_input_file.txt')
        sentences = utils.extract_sentences(input_file_path)
        self.assertIsNone(sentences)

    def test_throttler_time_spent(self) -> None:
        throttler = utils.Throttler(max_req=1, period=0.01, lock=Lock())
        t0 = time.time()
        for _ in range(100):
            throttler.throttle()
        dt = time.time() - t0
        self.assertTrue(dt > 0.01 * 100)

    # @patch('translator.translator.Translator')
    # def test_translate_sentence(self, translator):
    #     translator.translate.return_value = 'test mock'
    #     input_queue = Queue()
    #     input_queue.put("test")
    #     throttler = Mock()
    #     output_queue = Queue()
    #     utils.translate_sentence(input_queue, throttler, 'en', output_queue)
    # FIXME:
