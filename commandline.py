# -*- coding: utf-8 -*-
"""
commandline.py 

parse commandline
"""
import argparse

class CommandlineError(Exception):
    pass

_program_description = "directory wormhole" 

def parse_commandline():
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
