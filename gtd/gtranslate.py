import argparse
import rpyc

from gtd.config import Config

parser = argparse.ArgumentParser(
    description='gtanslate 1.0: command line utility for translating text')
parser.add_argument(
    '-f', '--file', type=str, required=True,
    help='-f <filename>: path to input filename to be translated')
parser.add_argument(
    '-l', '--language', type=str, required=True,
    help='-l <lang>: output language, can be one of "en", "it" or "de"')

args = parser.parse_args()


def gtranslate() -> None:
    connection = rpyc.connect("localhost", Config.RPYC_PORT)
    connection.root.get_things_done(args.file, args.language)
    connection.close()
