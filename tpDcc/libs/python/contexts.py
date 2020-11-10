#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains utility contexts
"""

from __future__ import print_function, division, absolute_import

import time
import logging
import contextlib

LOGGER = logging.getLogger('tpDcc-libs-python')


@contextlib.contextmanager
def empty_decorator_context():
    """
    Empty context decorator
    """

    pass


class Timer(object):
    def __init__(self, description, logger=None):
        self._start = 0.0
        self._end = 0.0
        self._description = description
        self._logger = logger or LOGGER

    def __enter__(self):
        self._start = time.time()

    def __exit__(self, *args, **kwargs):
        self._end = time.time()
        self._logger.info("{}: {}".format(self._description, (self._end - self._start)))
