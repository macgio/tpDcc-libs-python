import os
import sys
import ast
import time
from collections import OrderedDict

if sys.version_info[:2] > (2, 7):
    from importlib import configparser as ConfigParser
else:
    import ConfigParser

from tpQtLib.Qt.QtCore import *
from tpQtLib.Qt.QtWidgets import *

import tpRigToolkit as tp
from tpPyUtils import fileio, path, jsonio


class FileSettings(object):
    def __init__(self):
        self.directory = None
        self.file_path = None

        self.settings_dict = OrderedDict()
        self.write = None

    # region Public Functions
    def get(self, name):
        """
        Get a stored setting
        :param name: str, name of the setting to retrieve. Returns None, if setting is not found
        :return: variant, None || str
        """

        if name in self.settings_dict:
            return self.settings_dict[name]

    def set(self, name, value):
        """
        Set the value of a specific setting. If the setting does not exists, the setting is created with the
        given value
        :param name: str, name of the setting
        :param value: varinat, value of the setting
        """

        self.settings_dict[name] = value
        self._write()

    def get_settings(self):
        """
        Returns a list with all the settings stored
        :return: list<list<str, variant>>
        """

        found = list()
        for setting in self.settings_dict.keys():
            found.append([setting, self.settings_dict[setting]])

        return found

    def get_file(self):
        """
        Retuns the file path of the settings file
        :return: str
        """

        return self.file_path

    def set_directory(self, directory, filename='settings.cfg'):
        """
        Set the file that is used to stored settins on file
        :param directory: str
        :param filename: str
        :return: str
        """

        self.directory = directory
        self.file_path = fileio.create_file(filename=filename, directory=directory)
        self._read()

        return self.file_path

    def has_setting(self, name):
        """
        Returns if a specific name is stored
        :param name: str, name of the setting
        :return: bool
        """

        return name in self.settings_dict

    def has_settings(self):
        """
        Returns if there are settings stored or not
        :return: bool
        """

        if self.settings_dict:
            return True
        return False

    def reload(self):
        """
        Forces the reading of the settings
        """

        self._read()

    def clear(self):
        """
        Cleans the stored settings
        """

        self.settings_dict = OrderedDict()
        self._write()
    # endregion

    # region Private Functions
    def _read(self):
        """
        Internal function used to read settings from file
        """
        if not self.file_path:
            return

        lines = fileio.get_file_lines(self.file_path)
        if not lines:
            return

        self.settings_dict = OrderedDict()

        for line in lines:
            if not line:
                continue
            split_line = line.split('=')
            name = split_line[0].strip()
            value = split_line[-1]
            if not value:
                continue
            value = path.clean_path(value)
            try:
                value = eval(str(value))
            except Exception:
                value = str(value)

            self.settings_dict[name] = value

    def _write(self):
        """
        Internal function that writes stored settings into text file
        """

        lines = list()
        for key in self.settings_dict.keys():
            value = self.settings_dict[key]
            if type(value) == str or type(value) == unicode:
                value = '"{}"'.format(value)
            if value is None:
                value = 'None'
            line = '{0} = {1}'.format(key, str(value))
            lines.append(line)

        write = fileio.FileWriter(file_path=self.file_path)
        try:
            write.write(lines)
        except Exception:
            tp.logger.debug('Impossible to write in {}'.format(self.file_path))
            time.sleep(.1)
            write.write(lines)


class JSONSettings(FileSettings, object):
    def __init__(self):
        super(JSONSettings, self).__init__()

    # region Override Functions
    def set_directory(self, directory, filename='settings.json'):
        self.directory = directory

        # Check that given file name is a valid JSON file
        if not filename.endswith('.json'):
            old = path.join_path(directory, filename)
            if path.is_file(old):
                self.file_path = old
                self._read()
                return

        self.file_path = fileio.create_file(filename=filename, directory=directory)

        self._read()

        return self.file_path

    def _write(self):
        """
        Override function to add support to write JSON files
        """

        file_path = self._get_json_file()
        if not file_path:
            return

        writer = fileio.FileWriter(file_path)
        writer.write_json(self.settings_dict.items())

    def _read(self):
        """
        Override function to add support to read JSON files
        """

        if not self._has_json_file():
            self.settings_dict = OrderedDict()
            return

        file_path = self._get_json_file()
        if not file_path:
            return
        self.file_path = file_path

        try:
            data = OrderedDict(jsonio.read_file(file_path))
        except Exception:
            self.settings_dict = OrderedDict()
            return

        self.settings_dict = data
    # endregion

    # region Private Functions
    def _get_json_file(self):
        """
        Internal function that returns JSON file where settings are stored
        :return: str
        """

        if not self.file_path:
            return

        settings_directory = path.get_dirname(self.file_path)
        name = path.get_basename(self.file_path, with_extension=False)
        file_path = fileio.create_file(name+'.json', settings_directory)
        if not file_path:
            test_path = path.join_path(settings_directory, name+'.json')
            if path.is_file(test_path):
                file_path = test_path

        return file_path

    def _has_json_file(self):
        """
        Checks if the JSON file where settings should be stored exists or not
        :return: bool
        """

        if not self.file_path:
            return False

        settings_directory = path.get_dirname(self.file_path)
        name = path.get_basename(self.file_path, with_extension=False)
        file_path = path.join_path(settings_directory, name+'.json')
        if path.is_file(file_path):
            return True

        return False
    # endregion


class INISettings(object):
    def __init__(self, filename):
        """
        Constructor
        :param filename: str, INI filename
        """

        self._file = filename
        self._parser = ConfigParser.RawConfigParser()
        self._is_dirty = False
        try:
            self._parser.read(self._file)
        except Exception:
            tp.logger.warning('Impossible to read INI config file "{}"'.format(filename))
        self._section = list()

    def __enter__(self):
        """
        Utility function to be used with Python 'with' functino
        """

        return self

    def __exit__(self, type_, value, tb):
        """
        Utility function bo be used with Python 'with' function. Release the raw file and parser
        """

        self.close()
        return False

    def get_section(self):
        """
        Returns the current stack's section
        """

        return self._section[len(self._section) - 1].upper() if self._section else None

    section = property(get_section)

    def save(self):
        """
        Writes INI file to disk
        """

        if self._is_dirty:
            if not os.path.exists(os.path.dirname(self._file)):
                os.makedirs(os.path.dirname(self._file))

            with open(self._file, 'w') as f:
                self._parser.write(f)

        self._is_dirty = False

    def show_in_explorer(self):
        """
        Displays the INI file explorer
        """

        import subprocess
        subprocess.Popen(r'explorer /select, {0}'.format(self._file))

    def get(self, section, option, default, eval_=False):
        """
        Returns the value associated with a key in a section
        :param section: str, section containing the key
        :param option: str, key to use in retrieval
        :param default: object, value to use if the key is not defined
        :param eval_: bool, if True, will attempt to evaluate the string returned into a Python type
        :return: variant, associated value if successful; value passed in as default otherwise
        """

        if self._parser.has_section(section) and self._parser.has_option(section, option):
            if isinstance(default, bool):
                return self._parser.getboolean(section, option)
            if isinstance(default, float):
                return self._parser.getfloat(section, option)
            if isinstance(default, (int, long)):
                return self._parser.getint(section, option)
            if eval_:
                return ast.literal_eval(self._parser.get(section, option))
            return self._parser.get(section, option)
        return default

    def set(self, section, option, value):
        """
        Sets the value with an associated key in the respective section
        :param section: str, section containing the key
        :param option: str, key to use in storing the value
        :param value: object, value to store
        """

        if section:
            if not self._parser.has_section(section):
                self._parser.add_section(section)
            self._parser.set(section, option, str(value))
            self._is_dirty = True

    def remove(self, section, option):
        """
        Removes a key in a section
        :param section: str, section containing the key
        :param option: str, key to remove
        :return: bool, True if successful or False, otherwise
        """

        success = False
        if section:
            if self._parser.has_section(section):
                success = self._parser.remove_option(section, option)

        if success:
            self._is_dirty = True

        return success

    def push_section(self, section):
        """
        Pushes a new section onto the section stack
        :param section: str, INI section to push
        :return: str
        """

        self._section.append(section)

    def pop_section(self):
        """
        Removes the current section from the section stack
        :return: str
        """

        self._section.pop()

    def import_option(self, option, default, eval_=False):
        """
        Returns the value associated with a key in the section at the top of the section stack
        :param option: str, key to use in retrieval
        :param default: str, value to use if the key is not defined
        :param eval_: bool, if True, will attempt to evaluate the string returned into a Python type
        :return: associated value if successful or the value passed in as default otherwise
        """

        return self.get(self.section, option, default, eval_)

    def delete_option(self, option):
        """
        Removes the associated key in the section at the top of the section stack
        :param option: key to use in storing the value
        """

        return self.remove(self.section, option)

    def export_option(self, option, value):
        """
        Sets the value with an associated key in the section at the top of the stack's section
        :param option: str, key to use in storing the value
        :param value: value to store
        """

        self.set(self.section, option, value)

    def export_widget(self, option, widget):
        """
        Serializes a widget's state to an option, value pair Sets the value with an associated key in the section at the top of the section stack.

        :param str option:   The key to use in storing the value.
        :param str widget:   The QWidget to extractvalue to store.
        """

        if isinstance(widget, QComboBox):
            self.export_option(option, widget.currentIndex())
        elif isinstance(widget, QCheckBox):
            self.export_option(option, widget.isChecked())
        elif isinstance(widget, QToolButton):
            if widget.isCheckable():
                self.export_option(option, widget.isChecked())
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            self.export_option(option, widget.value())
        elif isinstance(widget, QLineEdit):
            self.export_option(option, widget.text())
        elif isinstance(widget, (QSize, QPoint)):
            self.export_option(option, widget.toTuple())
        else:
            assert False, "Unknown control type"

    def import_widget(self, option, widget):
        """
        Serializes a widget's state to an option, value pair Sets the value with an associated key in the section at the top of the section stack.

        :param str option:   The key to use in storing the value.
        :param str widget:   The QWidget to extractvalue to store.
        """

        if isinstance(widget, QComboBox):
            d = 0 if (widget.currentIndex() < 0) else widget.currentIndex()
            v = self.import_option(option, d)
            widget.setCurrentIndex(v)
        elif isinstance(widget, QCheckBox):
            d = widget.isChecked()
            v = self.import_option(option, d)
            widget.setChecked(v)
        elif isinstance(widget, QToolButton):
            if widget.isCheckable():
                d = widget.isChecked()
                v = self.import_option(option, d)
                widget.setChecked(v)
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            d = widget.value()
            v = self.import_option(option, d)
            widget.setValue(v)
        elif isinstance(widget, QLineEdit):
            d = widget.text()
            v = self.import_option(option, d)
            widget.setText(v)
        elif isinstance(widget, QSize):
            d = widget.toTuple()
            v = self.import_option(option, d, True)
            widget.setWidth(v[0])
            widget.setHeight(v[1])
        elif isinstance(widget, QPoint):
            d = widget.toTuple()
            v = self.import_option(option, d, True)
            widget.setX(v[0])
            widget.setY(v[1])
        else:
            assert False, "Unknown control type"

    def close(self):
        """
        Closes INI file
        """

        self.save()
        self._parser = None


class QtIniSettings(QSettings, object):
    def __init__(self, filename, window, max_files=10,):
        super(QtIniSettings, self).__init__(filename, QSettings.IniFormat, window)

        self._max_files = max_files
        self._window = window
        self._groups = [window.objectName(), 'RecentFiles']
        self._initialize()

    # region Properties
    def has_setting(self, setting_name):
        return self.get(setting_name)

    def get(self, setting_name):
        """
        Returns the setting stored with the given name
        :param setting_name: str
        :return:
        """

        return self.value(setting_name)

    def set(self, setting_name, setting_value):
        """
        Stores a new settings with the given name and the given value
        If the given setting already exists, it will be overwrited
        :param setting_name: str, setting name we want store
        :param setting_value: variant, setting value we want to store
        """

        self.setValue(setting_name, setting_value)

    def get_groups(self):
        """
        Returns the current preferences groups
        :return: list
        """

        return self._groups

    groups = property(get_groups)
    # endregion

    # region Public Functions
    def add_group(self, group):
        """
        Add a group to the current preferences groups
        :param group: str, name of group to add
        :return: bool, True if the group was successfully added
        """

        if group not in self._groups:
            self._groups.append(group)
            return True

        return False

    def remove_group(self, group):
        """
        Remove a group from the preferences group
        :param group: str, name of group to remove
        :return: bool, True if the group was successfully removed
        """

        if group in self._groups:
            self._groups.remove(group)
            return True

        return False

    def window_keys(self):
        """
        Returns a list of all window keys to save for layouts or rebuilding last layout on launch
        :return: list
        """

        if self._window is None:
            return []

        result = [self._window.objectName()]
        for dock in self._window.findChildren(QDockWidget):
            dock_name = dock.objectName()
            result.append(str(dock_name))

        return result

    def prefs_keys(self):
        """
        Returns a list of preferences keys
        :return: list<str>, list of user prefs keys
        """

        results = list()
        self.beginGroup('Preferences')
        results = self.childKeys()
        self.endGroup()
        return results

    def get_layouts(self):
        """
        Returns a list of window layout names
        :return: list
        """

        layout_names = list()
        layout_keys = ['%s/geometry' % x for x in self.window_keys()]

        for k in self.allKeys():
            if 'geometry' in k:
                attrs = k.split('/geometry/')
                if len(attrs) > 1:
                    layout_names.append(str(attrs[-1]))

        return sorted(list(set(layout_names)))

    def save_layout(self, layout):
        """
        Save a named layout
        :param layout: str, layout name to save
        """

        sys.utils.logger.info('Saving Layout: "{}"'.format(layout))
        self.setValue(self._window.objectName()+'/geometry/%s' % layout, self._window.saveGeoemtry())
        self.setValue(self._window.objectName()+'/windowState/%s' % layout, self._window.saveState())

        for dock in self._window.findChildren(QDockWidget):
            dock_name = dock.objectName()
            self.setValue('%s/geometry/%s' % (dock_name, layout), dock.saveGeometry())

    def restore_layout(self, layout):
        """
        Restore a named layout
        :param layout: str, layout name to restores
        """

        sys.utils.logger.info('Restoring layout: "{}"'.format(layout))
        window_keys = self.window_keys()

        for widget_name in window_keys:
            key_name = '%s/geometry/%s' % (widget_name, layout)
            if widget_name != self._window.objectName():
                dock = self._window.findChildren(QDockWidget, widget_name)
                if dock:
                    if key_name in self.allKeys():
                        value = self.value(key_name)
                        dock[0].restoreGeometry(value)
            else:
                if key_name in self.allKeys():
                    value = self.value(key_name)
                    self._window.restoreGeometry(value)

                window_state = '%s/windowState/%s' % (widget_name, layout)
                if window_state in self.allKeys():
                    self._window.restoreState(self.value(window_state))

    def delete_layout(self, layout):
        """
        Delete a named layout
        :param layout: str, layout name to restore
        """

        sys.utils.logger.info('Deleting layout: "{}"'.format(layout))
        window_keys = self.window_keys()

        for widget_name in window_keys:
            key_name = '%s/geometry/%s' % (widget_name, layout)
            if key_name in self.allKeys():
                self.remove(key_name)

            if widget_name == self._window.objectName():
                window_state = '%s/windowState/%s' % (widget_name, layout)
                if window_state in self.allKeys():
                    self.remoev(window_state)

    def get_default_value(self, key, *groups):
        """
        Returns the default values for a group
        :param key: str, key to search for
        :return: variant, default value of key (None if not found)
        """

        if self.group():
            try:
                self.endGroup()
            except:
                pass

        result = None
        group_name = groups[0]
        for group in groups[1:]:
            group_name += '/%s' % group

        group_name += '/%s' % 'default'
        group_name += '/%s' % key

        if group_name in self.allKeys():
            result = self.value(group_name)

        return result

    def delete_file(self):
        """
        Delete the preferences file on disk
        """

        sys.utils.logger.info('Deleting Settings: "{}"'.format(self.fileName()))
        return os.remove(self.fileName())

    def get_recent_files(self):
        """
        Get a tuple of the most recent files
        """

        recent_files = list()
        cnt = self.beginReadArray('RecentFiles')
        for i in range(cnt):
            self.setArrayIndex(i)
            fn = self.value('file')
            recent_files.append(fn)
        self.endArray()

        return tuple(recent_files)

    def add_recent_file(self, filename):
        """
        Adds a recent file to the stack
        :param filename: str, file name to add
        """

        recent_files = self.get_recent_files()
        if filename in recent_files:
            recent_files = tuple(x for x in recent_files if x != filename)

        recent_files = recent_files + (filename,)
        self.beginWriteArray('RecentFiles')
        for i in range(len(recent_files)):
            self.setArrayIndex(i)
            self.setValue('file', recent_files[i])
        self.endArray()

    def clear_recent_files(self):
        self.remove('RecentFiles')
    # endregion

    # region Private Functions
    def _initialize(self):
        window_name = self._window.objectName().upper()
        if window_name not in self.childGroups():
            if self._window is not None:
                self.setValue(window_name+'/geometry/default', self._window.saveGeometry())

                if isinstance(self._window, QMainWindow):
                    self.setValue(window_name+'/windowState/default', self._window.saveState())

        if 'RecentFiles' not in self.childGroups():
            self.beginWriteArray('RecentFiles', 0)
            self.endArray()

        while self.group():
            self.endGroup()
