import os
import signal
import sys
from subprocess import call


def my_signal_handler(*args):
    if os.environ.get('RUN_MAIN') == 'true':
        print('stopped'.upper())
        call('killall mjpg_streamer', shell=True)
        print('All mjpg_streamer stopped!'.upper())

    sys.exit(0)

signal.signal(signal.SIGINT, my_signal_handler)
