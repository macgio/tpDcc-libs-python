import math


class BaseVector(object):
    pass


class Vector2D(object):
    def __init__(self, x=1.0, y=1.0):
        self.x = None
        self.y = None

        if type(x) == list or type(x) == tuple:
            self.x = x[0]
            self.y = x[1]

        if type(x) == float or type(x) == int:
            self.x = x
            self.y = y

        self.magnitude = None

    def _add(self, value):
        if type(value) == float or type(value) == int:
            return Vector2D(self.x + value, self.y + value)

        if type(self) == type(value):
            return Vector2D(value.x + self.x, value.y + self.y)

        if type(value) == list:
            return Vector2D(self.x + value[0], self.y + value[1])

    def _sub(self, value):
        if type(value) == float or type(value) == int:
            return Vector2D(self.x - value, self.y - value)

        if type(self) == type(value):
            return Vector2D(self.x - value.x, self.y - value.y)

        if type(value) == list:
            return Vector2D(self.x - value[0], self.y - value[1])

    def _rsub(self, value):
        if type(value) == float or type(value) == int:
            return Vector2D(value - self.x, value - self.y - value)

        if type(self) == type(value):
            return Vector2D(value.x - self.x, value.y - self.y)

        if type(value) == list:
            return Vector2D(value[0] - self.x, value[1] - self.y)

    def _mult(self, value):
        if type(value) == float or type(value) == int:
            return Vector2D(self.x * value, self.y * value)

        if type(self) == type(value):
            return Vector2D(value.x * self.x, value.y * self.y)

        if type(value) == list:
            return Vector2D(self.x * value[0], self.y * value[1])

    def _divide(self, value):
        if type(value) == float or type(value) == int:
            return Vector2D(self.x / value, self.y / value)

        if type(self) == type(value):
            return Vector2D(value.x / self.x, value.y / self.y)

        if type(value) == list:
            return Vector2D(self.x / value[0], self.y / value[1])

    def __add__(self, value):
        return self._add(value)

    def __radd__(self, value):
        return self._add(value)

    def __sub__(self, value):
        return self._sub(value)

    def __rsub__(self, value):
        return self._sub(value)

    def __mul__(self, value):
        return self._mult(value)

    def __rmul__(self, value):
        return self._mult(value)

    def __call__(self):
        return [self.x, self.y]

    def __div__(self, value):
        return self._divide(value)

    def _reset_data(self):
        self.magnitude = None

    def normalize(self, in_place=False):
        if not self.magnitude:
            self.magnitude()

        vector = self._divide(self.magnitude)

        if in_place:
            self.x = vector.x
            self.y = vector.y
            self._reset_data()

        if not in_place:
            return vector

    def get_vector(self):
        return [self.x, self.y]

    def get_magnitude(self):
        self.magnitude = math.sqrt((self.x * self.x) + (self.y * self.y))
        return self.magnitude

    def get_distance(self, x=0.0, y=0.0):
        other = Vector2D(x, y)

        offset = self - other

        return offset.get_magnitude()


class Vector(object):
    def __init__(self, x=1.0, y=1.0, z=1.0):

        self.x = None
        self.y = None
        self.z = None

        x_test = x

        if type(x_test) == list or type(x_test) == tuple:
            self.x = x[0]
            self.y = x[1]
            self.z = x[2]

        if type(x_test) == float or type(x_test) == int:
            self.x = x
            self.y = y
            self.z = z

    def _add(self, value):
        if type(value) == float or type(value) == int:
            return Vector(self.x + value, self.y + value, self.z + value)

        if type(self) == type(value):
            return Vector(value.x + self.x, value.y + self.y, value.z + self.z)

        if type(value) == list:
            return Vector(self.x + value[0], self.y + value[1], self.z + value[2])

    def _sub(self, value):
        if type(value) == float or type(value) == int:
            return Vector(self.x - value, self.y - value, self.z - value)

        if type(self) == type(value):
            return Vector(self.x - value.x, self.y - value.y, self.z - value.z)

        if type(value) == list:
            return Vector(self.x - value[0], self.y - value[1], self.z - value[2])

    def _rsub(self, value):
        if type(value) == float or type(value) == int:
            return Vector(value - self.x, value - self.y - value, value - self.z)

        if type(self) == type(value):
            return Vector(value.x - self.x, value.y - self.y, value.z - self.z)

        if type(value) == list:
            return Vector(value[0] - self.x, value[1] - self.y, value[2] - self.z)

    def _mult(self, value):
        if type(value) == float or type(value) == int:
            return Vector(self.x * value, self.y * value, self.z * value)

        if type(self) == type(value):
            return Vector(value.x * self.x, value.y * self.y, value.z * self.z)

        if type(value) == list:
            return Vector(self.x * value[0], self.y * value[1], self.z * value[2])

    def __add__(self, value):
        return self._add(value)

    def __radd__(self, value):
        return self._add(value)

    def __sub__(self, value):
        return self._sub(value)

    def __rsub__(self, value):
        return self._sub(value)

    def __mul__(self, value):
        return self._mult(value)

    def __rmul__(self, value):
        return self._mult(value)

    def __call__(self):
        return [self.x, self.y, self.z]

    def get_vector(self):
        return [self.x, self.y, self.z]

    def list(self):
        return self.get_vector()


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


def get_distance(vector1, vector2):
    """
    Returns the distance between two vectors
    :param vector1: list<float, float, float>, vector
    :param vector2: list<float, float, float>, vector
    :return: float
    """

    v1 = Vector(vector1)
    v2 = Vector(vector2)
    v = v1 - v2
    dst = v()

    return math.sqrt(dst[0] * dst[0]) + (dst[1] * dst[1]) + (dst[2] * dst[2])
