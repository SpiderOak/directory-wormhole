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
import argparse
import logging
import logging.handlers
import sys

class CommandlineError(Exception):
    pass

_max_log_size = 16 * 1024 * 1024
_max_log_backup_files = 1000
_log_format_template = "%(asctime)s %(levelname)-8s %(name)-20s: %(message)s"
_program_description = "directory wormhole" 

def _initialize_stderr_logging():
    """
    log errors to stderr
    """                                                   
    log_level = logging.WARN                                                    
    handler = logging.StreamHandler(stream=sys.stderr)                          
    formatter = logging.Formatter(_log_format_template)                         
    handler.setFormatter(formatter)                                             
    handler.setLevel(log_level)                                                 
    logging.root.addHandler(handler)                      

    logging.root.setLevel(log_level)

def _initialize_file_logging(log_path, verbose):
    """
    initialize the permanent log
    """
    log_level = (logging.DEBUG if verbose else logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        log_path,
        mode="a", 
        maxBytes=_max_log_size,
        backupCount=_max_log_backup_files,
        encoding="utf-8"
    )
    formatter = logging.Formatter(_log_format_template)
    handler.setFormatter(formatter)

    logging.root.addHandler(handler)
    logging.root.setLevel(log_level)

def _parse_commandline():
    """
    organize program arguments
    """
    parser = argparse.ArgumentParser(description=_program_description)
    parser.add_argument("-l", "--log", dest="log_path", help="/path/to/logfile")
    parser.add_argument("-w", "--watch", dest="watch_path",  
                       help="/path/to/wormhole/directory") 
    parser.add_argument("-p", "--pattern", dest="pattern", default="*", 
                       help="glob pattern to watch for;for example, *.complete")
    parser.add_argument("-i", "--identity", dest="identity",
                       help="/path/to/motoboto_identity")
    parser.add_argument("-c", "--collection", dest="collection",
                       help="name_of_nimbus.io_collection")
    parser.add_argument("-a", "--archive-name-prefix", dest="prefix", default="",
                       help="prefix to prepend to the filename to upload")
    parser.add_argument("-v", "--verbose", action="store_true", default=False)

    args = parser.parse_args()

    if args.log_path is None:
        parser.print_help()
        raise CommandlineError("You must specify a log path")

    if args.watch_path is None:
        parser.print_help()
        raise CommandlineError("You must specify a directory to watch")

    return args

def main():
    """
    main entry point
    """
    _initialize_stderr_logging()
    log = logging.getLogger("main")

    try:
        args = _parse_commandline()
    except CommandlineError as instance:
        log.error("invalid commandline {0}".format(instance))
        return 1

    _initialize_file_logging(args.log_path, args.verbose)

    log.info("program starts")
    log.info("program terminates normally")
    return 0

if __name__ == "__main__":
    sys.exit(main())
