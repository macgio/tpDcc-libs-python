#! /usr/bin/env python

"""
Utility methods related to names and strings
"""

from __future__ import print_function, division, absolute_import, unicode_literals

# region Imports
import os
import re
import sys
import string
# endregion


# region Classes
class FindUniqueString(object):
    """
    Utility class to get unique strings
    """

    def __init__(self, test_string):
        self.test_string = test_string
        self.increment_string = None
        self.padding = 0

    # region Public Functions
    def set_padding(self, padding):
        self.padding = padding

    def get(self):
        return self._search()
    # endregion

    # region Private Functions
    def _get_scope_list(self):
        return []

    def _format_string(self, number):
        if number == 0:
            number = 1

        exp = search_last_number(self.test_string)

        if self.padding:
            number = str(number).zfill(self.padding)

        if exp:
            self.increment_string = '{0}{1}{2}'.fomat(self.test_string[:exp.start()], number, self.test_string[exp.end():])
        else:
            split_dot = self.test_string.split('.')
            if len(split_dot) > 1:
                split_dot[-2] += str(number)
                self.increment_string = string.join(split_dot, '.')
            elif len(split_dot) == 1:
                self.increment_string = '{0}{1}'.format(self.test_string, number)

    def _get_number(self):
        return get_end_number(self.test_string)

    def _search(self):
        number = self._get_number()
        self.increment_string = self.test_string
        unique = False

        while not unique:
            scope = self._get_scope_list()
            if not scope:
                unique = True
                continue
            if not self.increment_string in scope:
                unique = True
                continue
            if self.increment_string in scope:
                if not number:
                    number = 0
                self._format_string(number)
                number += 1
                unique = False
                continue

        return self.increment_string
    # endregion
# endregion


# region Functions
def remove_suffix(name):
    """
    Remove suffix from given name string
    @param name: string, given name string to process
    @return: string, name without suffix
    """

    # By convention, we split the names when we find a _ character
    edits = name.split('_')

    # If there is not a _ it means that there is not an underscore and we return the full name
    if len(edits) < 2:
        return name

    # The suffix will be _ + the last split string and the name will be the complete name without the suffix
    suffix = '_' + edits[-1]
    name_no_suffix = name[:-len(suffix)]

    return name_no_suffix


def get_numeric_name(text, names):

    from DccBox.dccutils import python as utils

    if text in names:
        text = re.sub('\\d*$', '', text)
        names = [n for n in names if n.startswith(text)]
        int_list = []
        for name in names:
            m = re.match('^%s(\\d+)' % text, name)
            if m:
                int_list.append(int(m.group(1)))
            else:
                int_list.append(0)

                int_list.sort()
        missing_int = utils.find_missing_items(int_list)
        if missing_int:
            _id = str(missing_int[0])
        else:
            _id = str(int_list[-1] + 1)
    else:
        _id = ''
    text += _id
    return text


def get_first_number(input_string, as_string=False):
    """
    Returns the first number of the given string
    :param input_string: str
    :param as_string: bool, Whether the found number should be returned as integer or as string
    :return: variant, str || int
    """

    found = re.search('[0-9]+', input_string)
    if not found:
        return None

    number_str = found.group()
    if not number_str:
        return None

    if as_string:
        return number_str
    number = int(number_str)

    return number


def get_last_number(input_string, as_string=False):
    """
    Returns the last number of the given string
    :param input_string: str
    :param as_string: bool, Whether the found number should be returned as integer or as string
    :return: variant, str || int
    """

    found = search_last_number(input_string)
    if not found:
        return None

    number_str = found.group()
    if not number_str:
        return None

    if as_string:
        return number_str
    number = int(number_str)

    return number


def get_end_number(input_string, as_string=False):
    """
    Get the number at the end of a string
    :param input_string: bool, Whether the found number should be returned as integer or as string
    :param as_string: bool, Whether the found number should be returned as integer or as string
    :return: variant, str || int,  number at the end of te string
    """

    found = re.findall('\d+', input_string)
    if not found:
        return None

    if type(found) == list:
        found = found[0]

    if as_string:
        return found
    else:
        return int(found)


def convert_side_name(name):
    """
    Convert a string with underscore "_\L", "_L0\_", "L\_", "_L" to "R". And vice and versa.
    :param name: str, string to convert
    :return: tuple of interger
    """

    if name == "L":
        return "R"
    elif name == "R":
        return "L"
    if name == 'l':
        return 'r'
    if name == 'r':
        return 'l'

    re_pattern = re.compile("_[RLrl][0-9]+_|^[RLrl][0-9]+_|_[RLrl][0-9]+$|_[RLrl]_|^[RLrl]_|_[RLrl]$")

    re_match = re.search(re_pattern, name)
    if re_match:
        instance = re_match.group(0)
        if instance.find("R") != -1:
            rep = instance.replace("R", "L")
        else:
            rep = instance.replace("L", "R")
        if instance.find('r') != -1:
            rep = instance.replace('r', 'l')
        else:
            rep = instance.replace('l', 'r')

        name = re.sub(re_pattern, rep, name)

    return name


def replace_string(string_value, replace_string, start, end):
    """
    Replaces one string by another
    :param string_value: str, string to replace
    :param replace_string: str, string to replace with
    :param start: int, string index to start replacing from
    :param end: int, string index to end replacing
    :return: str, new string after replacing
    """

    first_part = string_value[:start]
    second_part = string_value[end:]

    return first_part + replace_string + second_part


def replace_string_at_start(line, string_to_replace, replace_string):
    """
    Replaces string at the start of the given line
    :param line: str
    :param string_to_replace: str
    :param replace_string: str
    :return:
    """

    m = re.search('^%s' % string_to_replace, line)
    if not m:
        return

    start = m.start(0)
    end = m.end(0)
    new_line = line[:start] + replace_string + line[end:]

    return new_line


def replace_string_at_end(line, string_to_replace, replace_string):
    """
    Replaces string at the end of the given line
    :param line: str
    :param string_to_replace: str
    :param replace_string: str
    :return:
    """

    m = re.search('%s$' % string_to_replace, line)
    if not m:
        return

    start = m.start(0)
    end = m.end(0)
    new_line = line[:start] + replace_string + line[end:]

    return new_line


def clean_file_string(string):
    """
    Replaces all / and \\ characters by _
    :param string: str, string to clean
    :return: str, cleaned string
    """

    if string == '/':
        return '_'

    string = string.replace('\\', '_')

    return string


def clean_name_string(string_value, clean_chars='_', remove_char='_'):
    """
    Clean given string by cleaning given clean_char and removeing remove_chars
    :param string_value: str
    :param clean_chars: str
    :param remove_chars: str
    :return: str, cleaned name
    """

    string_value = re.sub('^[^A-Za-z0-9%s]+' % clean_chars, '', string_value)
    string_value = re.sub('[^A-Za-z0-9%s]+$' % clean_chars, '', string_value)
    string_value = re.sub('[^A-Za-z0-9]', remove_char, string_value)

    if not string_value:
        string_value = remove_char

    return string_value


def search_first_number(input_string):
    """
    Get the first number in a string
    :param input_string:  string to search for its first number
    :return: int, last number in the string
    """

    regex = re.compile('[0-9]+')
    return regex.search(input_string)


def search_last_number(input_string):
    """
    Get the last number in a string
    :param input_string:  string to search for its lsat number
    :return: int, last number in the string
    """

    regex = re.compile('(\d+)(?=(\D+)?$)')
    return regex.search(input_string)


def replace_last_number(input_string, replace_string):
    """
    Replace the last number with the given replace_string
    :param input_string: str, string to search for the last number
    :param replace_string: str, string to replace the last number with
    :return: str, new string after replacing
    """

    replace_string = str(replace_string)
    regex = re.compile('(\d+)(?=(\D+)?$)')
    search = regex.search(input_string)
    if not search:
        return input_string + replace_string
    else:
        return input_string[:search.start()] + replace_string + input_string[search.end():]


def increment_first_number(input_string, value=1):
    """
    Up the value of the first number by the given value (by default is 1)
    :param input_string: str, string to search for increment its first number
    :return: str, new string after the first number is replaced
    """

    search = search_first_number(input_string)
    if search:
        new_string = '{0}{1}{2}'.format(input_string[0:search.start()], int(search.group())+value, input_string[search.end():])
    else:
        new_string = input_string + '_{}'.format(value)

    return new_string


def increment_last_number(input_string, value=1):
    """
    Up the value of the last number by the given value (by default is 1)
    :param input_string: str, string to search for increment its last number
    :return: str, new string after the last number is replaced
    """

    search = search_last_number(input_string)
    if search:
        new_string = '{0}{1}{2}'.format(input_string[0:search.start()], int(search.group())+value, input_string[search.end():])
    else:
        new_string = input_string + '{}'.format(value)

    return new_string


def format_path(path):
    """
    Takes a path and format it to forward slashes
    :param path: str
    :return: str
    """

    return os.path.normpath(path).replace('\\', '/').replace('\t', '/t').replace('\n', '/n').replace('\a', '/a')


def add_unique_postfix(fn):
    if not os.path.exists(fn):
        return fn

    path, name = os.path.split(fn)
    name, ext = os.path.splitext(name)

    make_fn = lambda i: os.path.join(path, '%s_%d%s' % (name, i, ext))

    for i in range(2, sys.maxint):
        uni_fn = make_fn(i)
        if not os.path.exists(uni_fn):
            return uni_fn

    return None
# endregion
