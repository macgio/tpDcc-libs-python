#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains tests for tpDcc-libs-python
"""

import pytest

from tpDcc.libs.python import __version__


def test_version():
    assert __version__.get_version()
