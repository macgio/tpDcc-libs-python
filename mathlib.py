import math


class BaseVector(object):
    pass


class Vector2D(object):
    def __init__(self, x=1.0, y=1.0):
        self.x = None
        self.y = None

        if type(x) in [list, tuple]:
            self.x = x[0]
            self.y = x[1]

        if type(x) in [float, int]:
            self.x = x
            self.y = y

        self.magnitude = None

    def _add(self, value):
        if type(value) in [float, int]:
            return Vector2D(self.x + value, self.y + value)

        if type(self) == type(value):
            return Vector2D(value.x+self.x, value.y+self.y)

        if type(value) == list:
            return Vector2D(self.x+value[0], self.y+value[1])


def is_equal(x, y, tolerance=0.000001):
    """
    Checks if 2 float values are equal withing a given tolerance
    :param x: float, first float value to compare
    :param y: float, second float value to compare
    :param tolerance: float, comparison tolerance
    :return: bool
    """

    return abs(x-y) < tolerance


def lerp(start, end, alpha):
    """
    Computes a linear interpolation between two values
    :param start: start value to interpolate from
    :param end:  end value to interpolate to
    :param alpha: how far we want to interpolate (0=start, 1=end)
    :return: float, result of the linear interpolation
    """

    return start + alpha * (end - start)


def clamp(number, min_value, max_value):
    """
    Clamps a number between two values
    :param number: number, value to clamp
    :param min_value: number, maximum value of the number
    :param max_value: number, minimum value of the number
    :return: variant, int || float
    """

    return max(min(number, max_value), min_value)


def roundup(number, to):
    """
    Round up a number
    :param number: number to roundup
    :param to: number, mas value to roundup
    :return: variant, int || float
    """

    return int(math.ceil(number / to)) * to


def bounding_box_half_values(bbox_min, bbox_max):
    """
    Returns the values half way between max and min XYZ given tuples
    :param bbox_min: tuple, contains the minimum X,Y,Z values of the mesh bounding box
    :param bbox_max: tuple, contains the maximum X,Y,Z values of the mesh bounding box
    :return: tuple(int, int, int)
    """

    min_x, min_y, min_z = bbox_min
    max_x, max_y, max_z = bbox_max
    half_x = (min_x + max_x) * 0.5
    half_y = (min_y + max_y) * 0.5
    half_z = (min_z + max_z) * 0.5

    return half_x, half_y, half_z


def snap_value(input, snap_value):
    return round((float(input)/snap_value)) * snap_value