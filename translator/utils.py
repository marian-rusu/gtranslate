from collections import deque
from multiprocessing import Lock
from queue import Empty

from multiprocessing import Queue

from time import time, sleep

import logging
from pathlib import Path
from typing import Optional, List

from translator.g_translator import GTranslator
from translator.translator import Translator

LOGGER = logging.getLogger(__name__)


def extract_sentences(file_path: Path) -> Optional[List[str]]:
    """Extract all sentences from a file. Every not empty line is interpreted as a sentence."""
    if not file_path.is_file():
        LOGGER.info(f"There is no file with this path: {file_path}")
        return None

    with open(file_path, 'r') as input_file:
        sentences = [line.strip() for line in input_file.readlines() if line.strip()]
        return sentences


class Throttler:
    def __init__(self, max_req: int, period: float, lock: Lock) -> None:
        self._max_req = max_req
        self._period = period
        self._lock = lock
        self._last_request = time()
        self._request_timestamps = deque(maxlen=max_req)

    def throttle(self) -> None:
        with self._lock:
            t1 = time()
            self._request_timestamps.append(t1)
            if len(self._request_timestamps) >= self._max_req:
                t0 = self._request_timestamps[0]
                dt = t1 - t0
                if dt < self._period:
                    sleep(self._period - dt)


def translate_sentence(input_queue: Queue, throttler: Throttler, to_lang: str, output_queue: Queue) -> None:
    google_translator = GTranslator()
    translator = Translator(translator=google_translator)
    while True:
        try:
            s = input_queue.get(block=False)
        except Empty:
            break
        throttler.throttle()
        result = translator.translate(sentence=s, lang_tgt=to_lang)
        output_queue.put((s, result))
