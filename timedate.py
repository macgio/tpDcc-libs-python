#! /usr/bin/env python

"""
Module that contains utility functions related with time and date
"""


from __future__ import print_function, division, absolute_import, unicode_literals


# region Imports
import time
import datetime
# endregion


def convert_number_to_month(month_int):
    """
    Return a month as string given a month number
    :param month_int: int
    :return: str
    """

    months = ['January',
              'February',
              'March',
              'April',
              'May',
              'June',
              'July',
              'August',
              'September',
              'October',
              'November',
              'December']

    month_int -= 1
    if month_int < 0 or month_int > 11:
        return

    return months[month_int]


def get_current_time(date_and_time=True, reverse_date=False):
    """
    Returns current time
    :param date_and_time: bool, Whether to return only the time or time and data
    :param reverse_date: bool, Whether to return date with {year}-{month}-{day} format or {day}-{month}-{year} format
    :return: str
    """

    mtime = time.time()
    date_value = datetime.datetime.fromtimestamp(mtime)
    hour = str(date_value.hour)
    minute = str(date_value.minute)
    second = str(int(date_value.second))

    if len(hour) == 1:
        hour = '0'+hour
    if len(minute) == 1:
        minute = '0'+minute
    if len(second) == 1:
        second += '0'

    time_value = '{}:{}:{}'.format(hour, minute, second)

    if not date_and_time:
        return time_value
    else:
        year = date_value.year
        month = date_value.month
        day = date_value.day

        if reverse_date:
            return '{}-{}-{} {}'.format(year, month, day, time_value)
        else:
            return '{}-{}-{} {}'.format(day, month, year, time_value)


def get_current_date(reverse_date=False):
    """
    Returns current date
    :param reverse_date: bool, Whether to return date with {year}-{month}-{day} format or {day}-{month}-{year} format
    :return: str
    """

    mtime = time.time()
    date_value = datetime.datetime.fromtimestamp(mtime)
    year = date_value.year
    month = date_value.month
    day = date_value.day

    if reverse_date:
        return '{}-{}-{}'.format(year, month, day)
    else:
        return '{}-{}-{}'.format(day, month, year)
