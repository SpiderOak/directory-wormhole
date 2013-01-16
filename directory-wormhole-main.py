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
import os
import os.path
import queue
import sys
from threading import Event

import motoboto

from signal_handler import set_signal_handler
from log_setup import initialize_stderr_logging, initialize_file_logging
from commandline import parse_commandline, CommandlineError
from inotify_setup import create_notifier, create_notifier_thread, InotifyError
from archiver import archive_file, ArchiveError

def _initial_directory_scan(watch_path, file_name_queue):
    """
    load the queue with filenames found on startup
    """
    log = logging.getLogger("_initial_directory_scan")
    for file_name in os.listdir(watch_path):
        log.info("putting '{0}'".format(file_name))
        file_name_queue.put(file_name)

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

    if args.identity_path is not None:
        log.info("loading identity from {0}".format(args.identity_path))
        nimbusio_identity = \
            motoboto.identity.load_identity_from_file(args.identity_path)
        if nimbusio_identity is None:
            log.error("Unable to load identity from {0}".format(
                      args.identity_path))
            return 1
    else:
        nimbusio_identity = None

    halt_event = Event()
    set_signal_handler(halt_event)

    file_name_queue = queue.Queue()    

    try:
        notifier = create_notifier(args.watch_path, file_name_queue)
    except InotifyError as instance:
        log.error("Unable to initialize inotify: {0}".format(instance))
        return 1

    notifier_thread = create_notifier_thread(halt_event, notifier)
    notifier_thread.start()

    # we want the notifier running while we do the initial directory scan, so
    # we don't miss any files. But this leaves us open to duplicates()
    _initial_directory_scan(args.watch_path, file_name_queue)

    # so this eliminates duplicates, but leaks a little memory
    # if that's a problem, we could clean it out occasionally 
    file_name_set = set()

    log.info("main loop starts")
    return_code = 0
    while not halt_event.is_set():

        try:
            file_name = file_name_queue.get(block=True, timeout=1.0)
        except queue.Empty:
            continue

        log.debug("found file_name '{0}'".format(file_name))

        if args.pattern is not None:
            if not fnmatch.fnmatch(file_name, args.pattern):
                log.info("ignoring '{0}': does not match '{1}'".format(
                         file_name, args.pattern))
                continue

        if file_name in file_name_set:
            log.info("ignoring duplicate file name '{0}'".format(file_name))
            continue
        file_name_set.add(file_name)

        try:
            archive_file(args, nimbusio_identity, file_name)
            file_path = os.path.join(args.watch_path, file_name)
            log.info("deleting {0}".format(file_path))
            os.unlink(file_path)
        except Exception as instance:
            log.exception(instance)
            return_code = 1
            halt_event.set()

    log.info("main loop ends")
    notifier_thread.join(timeout=5.0)
#    assert not notifier_thread.is_alive
    notifier.stop()

    log.info("program terminates return_code = {0}".format(return_code))
    return return_code

if __name__ == "__main__":
    sys.exit(main())
