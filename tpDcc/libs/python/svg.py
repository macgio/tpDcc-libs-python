#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility methods related to write/read SVG files
"""

import os
import re
import logging
from collections import OrderedDict

from Qt.QtGui import *
from Qt.QtSvg import *

from pysvg import parser

LOGGER = logging.getLogger()


def get_svg_field_as_float(svg_field):
    """
    Converts SVG field to a float value
    :param svg_field: object
    :return: float
    """

    if not svg_field:
        svg_field = 0.0
    svg_field = str(svg_field)
    if 'px' in svg_field:
        svg_field = svg_field.strip('px')

    return float(svg_field)


def get_width_from_svg_file(svg_path):
    """
    Returns width of the given SVG file
    :param svg_path: str
    :return: float
    """

    if not os.path.isfile(svg_path):
        LOGGER.warning('Impossible to retrieve SVG width from file. SVG file "{}" does not exist!'.format(svg_path))
        return 0

    svg_obj = parse_svg(svg_path)
    svg_width = svg_obj.get_width()

    return svg_width


def get_height_from_svg_file(svg_path):
    """
    Returns height of the given SVG file
    :param svg_path: str
    :return: float
    """

    if not os.path.isfile(svg_path):
        LOGGER.warning('Impossible to retrieve SVG height from file. SVG file "{}" does not exist!'.format(svg_path))
        return 0

    svg_obj = parse_svg(svg_path)
    svg_height = svg_obj.get_height()

    return svg_height


def get_size_from_svg_file(svg_path):
    """
    Returns width and height of the given SVG file
    :param svg_path: str
    :return: tuple(float, float)
    """

    svg_size = [0, 0]
    if not os.path.isfile(svg_path):
        LOGGER.warning('Impossible to retrieve SVG size from file. SVG file "{}" does not exist!'.format(svg_path))
        return svg_size

    svg_obj = parse_svg(svg_path)
    svg_size[0] = svg_obj.get_width()
    svg_size[1] = svg_obj.get_height()

    return svg_size


def parse_svg(svg_path):
    """
    Parses given SVG file
    :param svg_path: str
    :return: SVG object
    """

    try:
        svg_obj = parser.parse(svg_path)
    except Exception as exc:
        raise Exception('{} | SVG file "{}" is not valid!'.format(exc, svg_path))

    return svg_obj


def get_svg_element_font_size(svg_elem):
    """
    Returns font size of the given SVG element
    :param svg_elem:
    :return: float
    """

    if 'style' in svg_elem._attributes:
        match = re.search(r'(font\-size\:(\d+\.?\d*)px\;)', svg_elem._attributes['style'])
        if not match:
            return float(svg_elem._attributes['font-size'])
        else:
            return float(match.groups()[1])
    else:
        font_size = svg_elem._attributes['font-size']
        if font_size.endswith('px'):
            font_size = font_size.replace('px', '')

        return float(font_size)


def set_svg_element_font_size(svg_elem, font_size):
    """
    Sets font size of the given SVG element
    :param svg_elem:
    :param font_size: float
    """

    if 'style' in svg_elem._attributes:
        match = re.search(r'(font\-size\:(\d+\.?\d*)px\;)', svg_elem._attributes['style'])
        if not match:
            svg_elem._attributes['font-size'] = font_size
        else:
            font_size_svg = match.groups()[0].replace(match.groups()[1], str(font_size))
            new_style = svg_elem._attributes['style'].replace(match.groups()[0], font_size_svg)
            svg_elem._attributes['style'] = new_style
    else:
        svg_elem._attributes['font-size'] = font_size


def convert_svg_to_bitmap(source, target):
    svg_renderer = QSvgRenderer(source)
    height = svg_renderer.defaultSize().height()
    width = svg_renderer.defaultSize().width()
    new_image = QImage(width, height, QImage.Format_ARGB32)
    painter = QPainter(new_image)
    svg_renderer.render(painter)
    new_image.save(target)
    painter.end()


class SvgNormalizer(object):
    """
    Normalizes each SVG element using original SVG resolution and new one
    """

    def __init__(self, svg_elem, new_resolution, svg_original_resolution):

        self._new_resolution = new_resolution
        self._original_resolution = svg_original_resolution

        if svg_elem.__class__.__name__ == 'rect':
            self._normalize_rect(svg_elem)
        elif svg_elem.__class__.__name__ == 'tspan':
            self._normalize_tspan(svg_elem)
        elif svg_elem.__class__.__name__ == 'text':
            self._normalize_text(svg_elem)
        elif svg_elem.__class__.__name__ == 'line':
            self._normalize_line(svg_elem)
        elif svg_elem.__class__.__name__ == 'path':
            self._normalize_path(svg_elem)
        elif svg_elem.__class__.__name__ == 'image':
            self._normalize_image(svg_elem)

    def _normalize_position(self, svg_elem):
        x_pos = get_svg_field_as_float(svg_elem._attributes.get('x'))
        y_pos = get_svg_field_as_float(svg_elem._attributes.get('y'))
        original_position = [x_pos, y_pos]
        new_x = round(self._new_resolution[0] * float(original_position[0]) / float(self._original_resolution[0]))
        new_y = round(self._new_resolution[1] * float(original_position[1]) / float(self._original_resolution[1]))
        svg_elem.set_x(new_x)
        svg_elem.set_y(new_y)

    def _normalize_size(self, svg_elem):
        svg_width = get_svg_field_as_float(svg_elem._attributes.get('width'))
        svg_height = get_svg_field_as_float(svg_elem._attributes.get('height'))
        original_size = [svg_width, svg_height]
        new_width = (self._new_resolution[0] * float(original_size[0]) / float(self._original_resolution[0]))
        new_height = (self._new_resolution[1] * float(original_size[1]) / float(self._original_resolution[1]))
        svg_elem.set_width(new_width)
        svg_elem.set_height(new_height)

    def _normalize_rect(self, svg_rect_elem):
        self._normalize_position(svg_rect_elem)
        self._normalize_size(svg_rect_elem)

    def _normalize_tspan(self, svg_tspan_elem):
        self._normalize_position(svg_tspan_elem)

    def _normalize_text(self, svg_text_elem):
        self._normalize_position(svg_text_elem)
        proportion = OrderedDict()
        proportion[2048] = 1
        proportion[1920] = 1
        proportion[1600] = 0.936
        proportion[1500] = 0.936
        proportion[1033] = 0.78
        proportion[1024] = 0.78
        proportion[960] = 0.74
        proportion[768] = 0.66
        proportion[640] = 0.60

        new_width = float(self._new_resolution[0])
        font_size = get_svg_element_font_size(svg_text_elem)
        for i in range(len(proportion.keys())):
            if new_width > proportion.keys()[i]:
                if i == 0:
                    font_proportion = new_width / proportion.keys()[0]
                else:
                    size_per_pixel = (proportion[proportion.keys()[i - 1]] - proportion[proportion.keys()[i]]) / \
                                     (proportion.keys()[i - 1] - proportion.keys()[i])
                    font_proportion = (
                            proportion[proportion.keys()[i]] + (new_width - proportion.keys()[i]) * size_per_pixel)
            break
        else:
            font_proportion = new_width * (proportion[proportion.keys()[
                len(proportion.keys()) - 1]] / proportion.keys()[len(proportion.keys()) - 1])

        new_font_size = font_size * font_proportion
        set_svg_element_font_size(svg_text_elem, new_font_size)

    def _normalize_line(self, svg_line_elem):
        x1_pos = get_svg_field_as_float(svg_line_elem._attributes.get('x1'))
        y1_pos = get_svg_field_as_float(svg_line_elem._attributes.get('y1'))
        original_position1 = [x1_pos, y1_pos]
        new_x1 = round(self._new_resolution[0] * float(original_position1[0]) / float(self._original_resolution[0]))
        new_y1 = round(self._new_resolution[1] * float(original_position1[1]) / float(self._original_resolution[1]))
        svg_line_elem._attributes['x1'] = new_x1
        svg_line_elem._attributes['y1'] = new_y1

        x2_pos = get_svg_field_as_float(svg_line_elem._attributes.get('x2'))
        y2_pos = get_svg_field_as_float(svg_line_elem._attributes.get('y2'))
        original_position2 = [x2_pos, y2_pos]
        new_x2 = round(self._new_resolution[0] * float(original_position2[0]) / float(self._original_resolution[0]))
        new_y2 = round(self._new_resolution[1] * float(original_position2[1]) / float(self._original_resolution[1]))
        svg_line_elem._attributes['x2'] = new_x2
        svg_line_elem._attributes['y2'] = new_y2

    def _normalize_path(self, svg_path_elem):
        path_x = float(svg_path_elem._attributes['d'].split(' ')[1].split(',')[0])
        path_y = float(svg_path_elem._attributes['d'].split(' ')[1].split(',')[1])
        dst_x = float(svg_path_elem._attributes['d'].split(' ')[2].split(',')[0])
        dst_y = float(svg_path_elem._attributes['d'].split(' ')[2].split(',')[1])
        width_proportion = (float(self._new_resolution[0]) / float(self._original_resolution[0]))
        height_proportion = (float(self._new_resolution[1]) / float(self._original_resolution[1]))
        new_path_x = path_x * width_proportion
        new_path_y = path_y * height_proportion
        new_dst_x = dst_x * width_proportion
        new_dst_y = dst_y * height_proportion
        new_d = 'm ' + str(new_path_x) + ', ' + str(new_path_y) + ' ' + str(new_dst_x) + ', ' + str(new_dst_y)
        svg_path_elem._attributes['d'] = new_d

    def _normalize_image(self, svg_image_elem):
        svg_width = get_svg_field_as_float(svg_image_elem._attributes.get('width'))
        svg_height = get_svg_field_as_float(svg_image_elem._attributes.get('height'))
        original_size = [svg_width, svg_height]
        aspect_ratio = float(svg_width) / float(svg_height)
        new_width = round(self._new_resolution[0] * float(original_size[0]) / float(self._original_resolution[0]))
        new_height = float(new_width) / aspect_ratio
        svg_image_elem.set_width(new_width)
        svg_image_elem.set_height(new_height)

        x_pos = get_svg_field_as_float(svg_image_elem._attributes.get('x'))
        y_pos = get_svg_field_as_float(svg_image_elem._attributes.get('y'))
        original_position = [x_pos, y_pos]
        x_dst_proportion = float(svg_width) / (float(original_position[0]) - x_pos)
        y_dst_proportion = float(svg_height) / (float(original_position[1]) - y_pos)
        new_x = self._new_resolution[0] - (new_width / x_dst_proportion)
        new_y = self._new_resolution[1] - (new_height / y_dst_proportion)
        svg_image_elem.set_x(new_x)
        svg_image_elem.set_y(new_y)
