#! /usr/bin/env python

"""
Module that contains utility functions related with apps
"""


from __future__ import print_function, division, absolute_import, unicode_literals


def is_in_nuke():
    """
    Checks if Nuke is available or not
    :return: bool
    """

    try:
        import nuke
        return True
    except ImportError:
        return False


def is_maya():
    """
    Checks if Maya is available or not
    :return: bool
    """

    try:
        import maya.cmds as cmds
        return True
    except ImportError:
        return False


def is_max():
    """
    Checks if Max is available or not
    :return: bool
    """

    try:
        import MaxPlus
        return True
    except ImportError:
        return False
