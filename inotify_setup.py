# -*- coding: utf-8 -*-
"""
inotify_setup.py 

setup inotify to watch directory
"""
import logging 

import pyinotify

class InotifyError(Exception):
    pass

class _ProcessEvent(pyinotify.ProcessEvent):
    
    def my_init(self, **kwargs):
        self._log = logging.getLogger("_ProcessEvent")
        self._log.info("max_queued_events = {0}".format(
            pyinotify.max_queued_events))
        self._event_handler = kwargs["event_handler"]

    def process_default(self, inotify_event):
        self._event_handler(inotify_event)

    def process_IN_Q_OVERFLOW(self, event):
        error_message = "Overflow: max_queued_events={0} {1}".format(
            pyinotify.max_queued_events, event,
        )
        self._log.error(error_message)
        raise InotifyError(error_message)

_incoming_files_mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_TO

def create_notifier(watch_path, event_handler):
    """
    create the inotifier infrastructure for watching a directory
    """
    log = logging.getLogger("create_notifier")
    watch_manager = pyinotify.WatchManager()

    log.info("watching path {0}".format(watch_path))
    result = watch_manager.add_watch(watch_path, 
                                     mask=_incoming_files_mask,
                                     rec=False, 
                                     auto_add=False, 
                                     quiet=False)
    if not watch_path in result:
        raise InotifyError("add_watch failed: invalid directory '{0}'".format(
            watch_path))

    if result[watch_path] < 0:
        raise InotifyError("add_watch failed: '{0}' {1}" % (watch_path, 
                                                            result[watch_path]))

    notifier = pyinotify.Notifier(watch_manager, 
                                  default_proc_fun= \
                                    _ProcessEvent(event_handler=event_handler))

    return notifier