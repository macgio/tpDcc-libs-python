#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for tpPyUtils
"""

from __future__ import print_function, division, absolute_import

import os
import sys


class tpPyUtils(object):
    def __init__(self):
        super(tpPyUtils, self).__init__()

        self.logger = self.create_logger()
        self.reload_all()

    @staticmethod
    def create_logger():
        """
        Creates and initializes tpPyUtils logger
        """

        from tpPyUtils import logger as logger_utils
        utils_log = logger_utils.Logger(name=tpPyUtils.__name__, level=logger_utils.LoggerLevel.DEBUG).logger
        utils_log.debug('Initializing tpPyUtils Logger ...')
        return utils_log

    @staticmethod
    def reload_all():
        # if os.environ.get('SOLSTICE_DEV_MODE', '0') == '1':
        import inspect
        scripts_dir = os.path.dirname(__file__)
        for key, module in sys.modules.items():
            try:
                module_path = inspect.getfile(module)
            except TypeError:
                continue
            if module_path == __file__:
                continue
            if module_path.startswith(scripts_dir):
                reload(module)


sys.utils = tpPyUtils()
sys.utils_log = sys.utils.logger
