import multiprocessing
import rpyc
from multiprocessing import Queue

from daemons import daemonizer
from pathlib import Path
from rpyc import ThreadedServer

from gtd.config import Config
from translator.utils import extract_sentences, Throttler, translate_sentence


class GTD(rpyc.Service):
    def on_connect(self, conn):
        print("connected")

    def on_disconnect(self, conn):
        print("disconnected")

    def exposed_get_things_done(self, input_file: str, to_lang: str = 'en') -> None:
        sentences_input_queue = Queue()
        throttler = Throttler(Config.QUERIES_PER_SEC, 1., multiprocessing.Lock())
        print(f"Translation daemon started, throttling at  {Config.QUERIES_PER_SEC} queries/second.")
        sentences = extract_sentences(Path(input_file))

        if not sentences:
            print(
                f"No sentence to translate! Check input file: "
                f"{input_file}")

        for sentence in sentences:
            sentences_input_queue.put(sentence)

        results_queue = Queue()
        cpu_count = multiprocessing.cpu_count()

        processes = []
        for _ in range(cpu_count):
            prc = multiprocessing.Process(target=translate_sentence,
                                          args=(sentences_input_queue,
                                                throttler,
                                                to_lang,
                                                results_queue))
            prc.start()
            processes.append(prc)

        for prc in processes:
            prc.join()

        while not results_queue.empty():
            res = results_queue.get()
            print(f'{res[0]} -> {res[1]}')


@daemonizer.run(pidfile="/tmp/sleepy.pid")
def start_daemon() -> None:
    t = ThreadedServer(GTD, port=Config.RPYC_PORT)
    t.start()
