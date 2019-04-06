#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains logger functionality
"""

from __future__ import print_function, division, absolute_import

import os
import logging

from tpPyUtils import osplatform


class LoggerLevel:
    def __init__(self):
        pass

    INFO = logging.INFO
    WARNING = logging.WARNING
    DEBUG = logging.DEBUG
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

class Logger(object):
    def __init__(self, name, level=LoggerLevel.INFO, record_temp_log=False):
        self._name = name
        self._level = level
        self._logger = None
        self._initialized = False
        self._record_temp_log = record_temp_log
        self.create()

    def create(self):
        """
        Creates new logger
        """

        format_ = '[%(asctime)s - %(levelname)s:]: %(name)s - %(message)s'

        try:
            logging.basicConfig(format=format_) if format_ else logging.basicConfig()
            self._logger = logging.getLogger(self._name)
            self._logger.setLevel(self._level)
            # hdlr = logging.FileHandler(self.get_log_file(),  mode='w')
            # formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            # hdlr.setFormatter(formatter)
            # self._logger.addHandler(hdlr)
        except Exception:
            logging.basicConfig(format=format_) if format_ else logging.basicConfig()
            self._logger = logging.getLogger(self._name)
            self._logger.setLevel(self._level)
            # hdlr = logging.FileHandler(self.get_log_file(), mode='w')
            # formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            # hdlr.setFormatter(formatter)
            # self._logger.addHandler(hdlr)

    def enable(self):
        """
        Enables debugging on the logger
        """

        self._level = logging.DEBUG
        self._logger.setLevel(self._level)

    def disable(self):
        """
        Disables debugging on the logger
        """

        self._level = logging.INFO
        self._logger.setLevel(self._level)

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)
        if self._record_temp_log:
            record_temp_log(self._name, 'DEBUG: {}'.format(msg))

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)
        if self._record_temp_log:
            record_temp_log(self._name, 'INFO: {}'.format(msg))

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, *args, **kwargs)
        if self._record_temp_log:
            record_temp_log(self._name, 'WARNING: {}'.format(msg))

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)
        if self._record_temp_log:
            record_temp_log(self._name, 'ERROR: {}'.format(msg))

    def log(self, lvl, msg, *args, **kwargs):
        self._logger.log(lvl, msg, *args, **kwargs)
        if self._record_temp_log:
            record_temp_log(self._name, 'LOG: {}'.format(msg))

    def exception(self, msg, *args, **kwargs):
        self._logger.exception(msg, *args, **kwargs)
        if self._record_temp_log:
            record_temp_log(self._name, 'EXCEPTION: {}'.format(msg))
    # endregion

    # region Private Functions
    def get_log_file(self, root_folder, log_extension='log'):
        """
        Returns log file
        :return: str
        """

        from tpPyUtils import osplatform

        return os.path.join(osplatform.get_system_config_directory(), root_folder, '{}.{}'.format(self._name, log_extension))

    # endregion


def start_temp_log(log_name):
    """
    Initializes a new temp and stores its results in environment variable
    :param log_name: str, name of the log
    """

    osplatform.set_env_var('{}_KEEP_TEMP_LOG'.format(log_name.upper()), 'True')
    osplatform.set_env_var('{}_TEMP_LOG'.format(log_name.upper()), '')


def record_temp_log(log_name, value):
    """
    Adds a new value to the temp log with the given name (if exists)
    :param log_name: str, name of the log we want to add value into
    :param value: str
    """

    if osplatform.get_env_var('{}_KEEP_TEMP_LOG'.format(log_name.upper())) == 'True':
        value = value.replace('\t', '  ') + '\n'
        osplatform.append_env_var('{}_TEMP_LOG'.format(log_name.upper()), value)


def end_temp_log(log_name):
    """
    Removes temp log with given name and returns its contents
    :param log_name: str, nam of the temp log we want to remove
    :return: str
    """

    osplatform.set_env_var('{}_KEEP_TEMP_LOG'.format(log_name.upper()), 'False')
    value = osplatform.get_env_var('{}_TEMP_LOG'.format(log_name.upper()))
    osplatform.set_env_var('{}_TEMP_LOG'.format(log_name.upper()), '')
    osplatform.set_env_var('{}_LAST_TEMP_LOG'.format(log_name.upper()), value)

    return value
