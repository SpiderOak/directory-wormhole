directory-wormhole
==================

The director wormhole is a simple Python3 program that watches a directory with inotify for files matching a glob pattern. When matching files exist, they are uploaded to Nimbus.io and then deleted. 

usage 
======

arguments::
    directory-wormhole-main.py [-h] [-l LOG_PATH] [-w WATCH_PATH]
                                      [-p PATTERN] [-i IDENTITY_PATH]
                                      [-c COLLECTION_NAME] [-a PREFIX] [-v]

    -h, --help            show this help message and exit
    -l LOG_PATH, --log LOG_PATH
                        /path/to/logfile
    -w WATCH_PATH, --watch WATCH_PATH
                        /path/to/wormhole/directory
    -p PATTERN, --pattern PATTERN
                        glob pattern to watch for;for example, *.complete
    -i IDENTITY_PATH, --identity IDENTITY_PATH
                        /path/to/motoboto_identity
    -c COLLECTION_NAME, --collection COLLECTION_NAME
                        name_of_nimbus.io_collection
    -a PREFIX, --archive-name-prefix PREFIX
                        prefix to prepend to the filename to upload
    -v, --verbose
