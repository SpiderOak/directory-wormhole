#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
directiory-wormhole-main.python

See SpiderOak Ticket #3032

The directory wormhole is a simple Python3 program that watches a directory with 
inotify for files matching a glob pattern. When matching files exist, 
they are uploaded to Nimbus.io and then deleted.

It uses these command line arguments:

 --log /path/to/logfile
 --watch /path/to/wormhole/directory 
 --pattern glob pattern to watch for. for example, *.complete
 --identity /path/to/motoboto_identity
 --collection name_of_nimbus.io_collection
 --archive-name-prefix prefix to prepend to the filename to upload
"""
import logging
import sys
from threading import Event

from signal_handler import set_signal_handler
from log_setup import initialize_stderr_logging, initialize_file_logging
from commandline import parse_commandline, CommandlineError
from inotify_setup import create_notifier, InotifyError

def _event_handler(inotify_event):
    log = logging.getLogger("_event_handler")
    log.info("{0}".format(inotify_event))

def main():
    """
    main entry point
    """
    initialize_stderr_logging()
    log = logging.getLogger("main")

    try:
        args = parse_commandline()
    except CommandlineError as instance:
        log.error("invalid commandline {0}".format(instance))
        return 1

    initialize_file_logging(args.log_path, args.verbose)

    halt_event = Event()
    set_signal_handler(halt_event)

    try:
        notifier = create_notifier(args.watch_path, _event_handler)
    except InotifyError as instance:
        log.error("Unable to initialize inotify: {0}".format(instance))

    log.info("main loop starts")
    return_code = 0
    while not halt_event.is_set():

        try:
            if notifier.check_events(timeout=10000):
                notifier.read_events()
                notifier.process_events()
        except Exception as instance:
            log.exception(instance)
            return_code = 1
            halt_event.set()

    log.info("main loop ends")
    notifier.stop()

    log.info("program terminates return_code = {0}".format(return_code))
    return return_code

if __name__ == "__main__":
    sys.exit(main())
