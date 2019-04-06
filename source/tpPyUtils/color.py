#! /usr/bin/env python

"""
Base class for QColor colors
"""


from __future__ import print_function, division, absolute_import, unicode_literals

# region Imports
import random

from Qt.QtGui import *
# endregion

# region Constants
_NUMERALS = '0123456789abcdefABCDEF'
_HEXDEC = {v: int(v, 16) for v in (x+y for x in _NUMERALS for y in _NUMERALS)}

# TODO: Change by enum
_LOWERCASE, _UPPERCASE = 'x', 'X'
# endregion


class Color(QColor, object):
    def __eq__(self, other):
        if other == self:
            return True
        elif isinstance(other, Color):
            return self.to_string() == other.to_string()
        else:
            return False

    # region Class Functions
    @classmethod
    def from_color(cls, color):
        """
        Gets a string formateed color from a QColor
        :param color: QColor, color to parse
        :return: (str)
        """

        color = ('rgb(%d, %d, %d, %d)' % color.getRgb())
        return cls.from_string(color)

    @classmethod
    def from_string(cls, text_color):
        """
        Returns a (int, int, int, int) format color from a string format color
        :param text_color: str, string format color to parse
        :return: (int, int, int, int)
        """

        a = 255
        try:
            r, g, b, a = text_color.replace('rgb(', '').replace(')', '').split(',')
        except ValueError:
            r, g, b = text_color.replace('rgb(', '').replace(')', '').split(',')

        return cls(int(r), int(g), int(b), int(a))

    @classmethod
    def rgb_from_hex(cls, triplet):
        """
        Returns a RGB triplet from an hexadecimal value
        :param triplet: r,g,b Hexadecimal Color tuple
        """

        return _HEXDEC[triplet[0:2]], _HEXDEC[triplet[2:4]], _HEXDEC[triplet[4:6]]

    @classmethod
    def hex_from_rgb(cls, rgb, lettercase=_LOWERCASE):
        """
        Returns a hexadecimal value from a triplet
        :param rgb: tuple(r,g,b) RGB Color tuple
        :param lettercase: LOWERCASE if you want to get a lowercase or UPPERCASE
        """

        return format(rgb[0] << 16 | rgb[1] << 8 | rgb[2], '06' + lettercase)

    @classmethod
    def rgb_to_hex(cls, rgb):
        """
        Returns RGB color from hexadecimal
        :param rgb:
        :return: str
        """

        return '#%02x%02x%02x' % rgb

    @classmethod
    def get_random_hex(cls, return_sign=True):
        """
        Returns a random HEX value
        :param return_sign: bool, True if you want to get color sign
        :return: str
        """

        r = lambda: random.randint(0, 255)
        if return_sign:
            return '#%02X%02X%02X' % (r(), r(), r())
        else:
            return '%02X%02X%02X' % (r(), r(), r())

    @classmethod
    def get_random_rgb(cls):
        """
        Returns a random RGB color
        """

        hex = cls.get_random_hex(return_sign=False)
        return cls.rgb_from_hex(hex)

    @classmethod
    def hex_to_qcolor(cls, hex_color):

        """
        Converts a Hexadecimal color to QColor
        """

        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return QColor(r, g, b)

    @classmethod
    def get_complementary_color(cls, color):

        """
        Returns the complementary color of the given color
        :param color: QColor
        """

        hsl_hue = color.hslHueF()
        hsl_saturation = color.hslSaturationF()
        lightness = color.lightnessF()
        lightness = 1.0 - lightness
        hsl_hue += 0.5
        if hsl_hue >= 1.0:
            hsl_hue -= 1.0
        return cls.fromHslF(hsl_hue, hsl_saturation, lightness)

    @classmethod
    def get_option_color(cls, option):
        """
        Returns QColor depending of the option passed as argument
        :param option: str, Option to get color
        """

        if option == 'Grey':
            color = cls.fromRgbF(0.4, 0.4, 0.4)
        elif option == 'Cancel':
            color = cls.fromRgbF(0.7, 0.5, 0.4)
        elif option == 'OK' or option == 'ok':
            color = cls.fromRgbF(0.5, 0.7, 0.8)
        elif option == 'Warning' or option == 'Warn':
            color = cls.fromRgbF(0.7, 0.2, 0.2)
        elif option == 'Collapse':
            color = cls.fromRgbF(0.15, 0.15, 0.15)
        elif option == 'Subtle':
            color = cls.fromRgbF(0.48, 0.48, 0.6)
        else:
            color = cls.fromRgbF(0.48, 0.48, 0.6)
        if option:
            color.ann = option + ' Color'
        return color

    @classmethod
    def expand_normalized_rgb(cls, normalized_rgb):
        return tuple([float(normalized_rgb[0]) * 255, float(normalized_rgb[1]) * 255, float(normalized_rgb[2]) * 255])

    @classmethod
    def normalized_rgb(cls, rgb):
        return tuple([float(rgb[0]) / 255, float(rgb[1]) / 255, float(rgb[2]) / 255])

    def to_string(self):
        """
        Returns the color with string format
        :return: str
        """

        return 'rgb(%d, %d, %d, %d)' % self.getRgb()

    def is_dark(self):
        """
        Return True if the color is considered dark (RGB < 125(mid grey)) or False otherwise
        :return: bool
        """

        return self.red() < 125 and self.green() < 125 and self.blue() < 125


class RubberRectColors(object):
    """
    Class that store predefined colors for rubber rects
    """

    BaseColor = QColor(255, 255, 255, 50)


class GridColors(object):
    """
    Class that store predefined colors for grids
    """

    BaseColor = QColor(60, 60, 60, 100)
    DarkerColor = QColor(20, 20, 20, 100)

# =================================================================================================================


DEFAULT_DARK_COLOR = Color(50, 50, 50, 255)
DEFAULT_LIGHT_COLOR = Color(180, 180, 180, 255)
BLACK = QColor(0.0, 0.0, 0.0)
GRAY = QColor(0.5, 0.5, 0.5)
RED = QColor(1.0, 0.0, 0.0)
GREEN = QColor(0.0, 1.0, 0.0)
BLUE = QColor(0.0, 0.0, 1.0)
YELLOW = QColor(1.0, 1.0, 0.0)
MAGENTA = QColor(1.0, 0.0, 1.0)
CYAN = QColor(0.0, 1.0, 1.0)
WHITE = QColor(1.0, 1.0, 1.0)
DARK_GRAY = QColor(0.25, 0.25, 0.25)
DARK_RED = QColor(0.75, 0.0, 0.0)
DARK_GREEN = QColor(0.0, 0.75, 0.0)
DARK_BLUE = QColor(0.0, 0.0, 0.75)
DARK_YELLOW = QColor(0.75, 0.75, 0.0)
DARK_MAGENTA = QColor(0.75, 0.0, 0.75)
DARK_CYAN = QColor(0.0, 0.75, 0.75)
LIGHT_GRAY = QColor(0.75, 0.75, 0.75)
LIGHT_RED = QColor(1.0, 0.25, 0.25)
LIGHT_GREEN = QColor(0.25, 1.0, 0.25)
LIGHT_BLUE = QColor(0.25, 0.25, 1.0)
LIGHT_YELLOW = QColor(1.0, 1.0, 0.25)
LIGHT_MAGENTA = QColor(1.0, 0.25, 1.0)
LIGHT_CYAN = QColor(0.25, 1.0, 1.0)

# =================================================================================================================


def convert_2_hex(color):
    hex = '#'
    for var in color:
        var = format(var, 'x')
        if len(var) == 1:
            hex += '0' + str(var)
        else:
            hex += str(var)

    return hex