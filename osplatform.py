#! /usr/bin/env python

"""
Utility methods related to cross-platform functionality
"""

# region Imports
import os
import sys
import getpass
import subprocess
# endregion


class Platforms(object):
    Windows = 'Windows'
    Linux = 'Linux'
    Mac = 'MacOSX'


def get_platform():
    pl = Platforms.Windows

    if 'linux' in sys.platform:
        pl = Platforms.Linux
    elif sys.platform == 'darwin':
        pl = Platforms.Mac

    return pl


def get_home_directory(platform):
    if platform == Platforms.Windows:
        os.environ['TMPDIR'] = os.getenv('TEMP')
        os.environ['HOME'] = os.getenv('HOMEPATH')
        return os.getenv('HOMEPATH')
    if platform == Platforms.Linux:
        return os.getenv('HOME')
    if platform == Platforms.Mac:
        return os.getenv('HOME')


def is_linux():
    """
    Check to see if current platform is Linux
    :return: bool
    """

    platform = get_platform()
    if platform == Platforms.Linux:
        return True
    return False


def is_mac():
    """
    Check to see if current platform is Mac
    :return: bool
    """

    platform = get_platform()
    if platform == Platforms.Mac:
        return True
    return False


def is_windows():
    """
    Check to see if current platform is Windows
    :return: bool
    """

    platform = get_platform()
    if platform == Platforms.Windows:
        return True
    return False


def get_user():
    """
    Returns the current user
    :return: str
    """

    return getpass.getuser()


def get_permission(filepath):
    """
    Returns the current permission level
    :param filepath: str
    """

    try:
        os.chmod(filepath, 0777)
    except:
        return


def init_env_var(name):
    """
    Initializes a new environment variable if the variable does not exists.
    If it does not exists, nothing happens
    :param name: str, name of the new environment variable
    """

    if name not in os.environ:
        os.environ[name] = ''


def set_env_var(name, value):
    """
    Set the value of an environment variable
    :param name: str, name of the environment variable to set
    :param value: variant, value to initialize environment variable with, empty string by default
    """

    if name not in os.environ:
        init_env_var(name)

    os.environ[name] = str(value)


def get_env_var(name):
    """
    Returns the value of an environment variable
    :param name: str, name of the environment variable
    """

    if name in os.environ:
        return os.environ[name]


def append_env_var(name, value):
    """
    Append string value to the end of the environment variable
    :param name: str, name of the environment variable to set
    :param value: variant, value to initialize environment variable with, empty string by default
    """

    env_value = get_env_var(name=name)
    env_value += str(value)
    set_env_var(name=name, value=env_value)


def add_to_PYTHONPATH(path):
    """
    Adds given path to the Python Path only if it is not already present in it
    :param path: str
    """

    if not path:
        return

    if not path in sys.path:
        sys.path.append(path)


def get_system_config_directory():
    """
    Returns platform specific configuration directory
    """

    if sys.platform.startswith('darwin'):
        config_directory = os.path.join(os.path.expanduser('~'), 'Library', 'Preferences')
    elif os.name == 'nt':
        config_directory = os.getenv('APPDATA') or os.path.expanduser('~')
    else:
        config_directory = os.getenv('XDG_CONFIG_HOME') or os.path.join(os.path.expanduser('~'), '.config')

    return config_directory


def open_folder(path):
    """
    Open folder using OS default settings
    :param path: str, folder path we want to open
    """

    if sys.platform.startswith('darwin'):
        subprocess.Popen(["open", path])
    elif os.name == 'nt':
        os.startfile(path)
    elif os.name == 'posix':
        subprocess.Popen(["xdg-open", path])
    else:
        raise NotImplementedError('OS not supported: {}'.format(os.name))


def open_file(file_path):
    """
    Open file using OS default settings
    :param file_path: str, file path we want to open
    """

    if sys.platform.startswith('darwin'):
        subprocess.call(('open', file_path))
    elif os.name == 'nt':
        os.startfile(file_path)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', file_path))
    else:
        raise NotImplementedError('OS not supported: {}'.format(os.name))

