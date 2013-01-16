# -*- coding: utf-8 -*-
"""
archiver.py 

code for archiving a file to nimbus.io
"""
import logging
import os.path

import motoboto
from motoboto.s3.key import Key

class ArchiveError(Exception):
    pass

def archive_file(args, nimbusio_identity, file_name):
    log = logging.getLogger("archive_file")

    s3_emulator = motoboto.connect_s3(nimbusio_identity)

    if args.collection_name is None:
        bucket = s3_emulator.default_bucket
    else:
        bucket = s3_emulator.get_bucket(args.collection_name)

    key_name = "".join([args.prefix, file_name])  
    archive_key = Key(bucket, key_name)

    log.info("archiving {0} as key {1} to collection {2}".format(file_name,
                                                                 archive_key,
                                                                 bucket))

    file_path = os.path.join(args.watch_path, file_name)
    with open(file_path, "rb") as input_file:
        archive_key.set_contents_from_file(input_file)
    log.info("archive successful version identifier = {0}".format(
             archive_key.version_id))    

    s3_emulator.close()
