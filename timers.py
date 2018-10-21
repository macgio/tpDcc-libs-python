#! /usr/bin/env python

"""
Module that contains different types of timers
"""

from __future__ import print_function, division, absolute_import, unicode_literals


# region Imports
import sys
import time
from Qt.QtCore import *
# endregion


class ClickTimer(QObject, object):
    EXECUTE = Signal()

    # region Methods
    def __init__(self):
        super(ClickTimer, self).__init__()
        self.timer_id = None
        self.init_data()

    def set_data(self, button, modifier, pos, selected):
        self.button = button
        self.modifier = modifier
        self.pos = pos
        self.isSelected = selected

    def init_data(self):
        self.button = None
        self.modifier = None
        self.pos = None
        self.isSelected = False

    def start(self, interval):
        self.timer_id = self.startTimer(interval)

    def remove_timer(self):
        if self.timer_id:
            self.killTimer(self.timer_id)
        self.timer_id = None
        return
    # endregion

    # region Override Methods
    def timerEvent(self, event):
        if self.timer_id == event.timerId():
            self.EXECUTE.emit()
        self.remove_timer()
    # endregion


class StopWatch(object):
    """
    Class that can be used to check how long a command takes to run
    """

    running = 0

    def __init__(self):
        self.time = None
        self.feedback = True

    def __del__(self):
        self.end()

    def start(self, description='', feedback=True):
        self.feedback = feedback
        if feedback:
            tabs = '\t' * self.running
            sys.utils_log.debug('{}started timer: {}'.format(tabs, description))
        self.time = time.time()
        if feedback:
            self.__class__.running += 1

    def end(self):
        if not self.time:
            return

        seconds = time.time() - self.time
        self.time = None

        seconds = round(seconds, 2)
        minutes = None
        if seconds > 60:
            minutes, seconds = divmod(seconds, 60)
            seconds = round(seconds, 2)
            minutes = int(minutes)

        if self.feedback:
            tabs = '\t' * self.running
            if minutes is None:
                sys.utils_log.debug('{}end timer: {} seconds'.format(tabs, seconds))
            else:
                if minutes > 1:
                    sys.utils_log.debug('{} end timer: {}  minutes, {} seconds'.format(tabs, minutes, seconds))
                elif minutes == 1:
                    sys.utils_log.debug('{} end timer: {} minute, {} seconds'.format(tabs, minutes, seconds))
            self.__class__.running -= 1

        return minutes, seconds

    def stop(self):
        return self.end()
