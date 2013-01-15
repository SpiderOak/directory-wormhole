# -*- coding: utf-8 -*-
"""
signal_handler.py

set up signal handler to set halt_event on SIGTERM
"""
import signal

def _create_signal_handler(halt_event):
    def cb_handler(*_):
        halt_event.set()
    return cb_handler

def set_signal_handler(halt_event):
    """
    set a signal handler to set halt_event when SIGTERM is raised
    """
    signal.signal(signal.SIGTERM, _create_signal_handler(halt_event))