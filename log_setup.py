# -*- coding: utf-8 -*-
"""
log_setup.py

set up logging
"""
import logging
import logging.handlers
import sys

_max_log_size = 16 * 1024 * 1024
_max_log_backup_files = 1000
_log_format_template = "%(asctime)s %(levelname)-8s %(name)-20s: %(message)s"

def initialize_stderr_logging():
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

def initialize_file_logging(log_path, verbose):
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

