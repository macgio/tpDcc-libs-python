#!/usr/bin/env python
# # -*- coding: utf-8 -*-
#
# """ ==================================================================
# Script Name: qtutils.py
# by Tomas Poveda
# Utility module that contains useful utilities functions for PySide
# ______________________________________________________________________
# ==================================================================="""

import os
import re
import subprocess

import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI
import shiboken2 as shiboken

from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt import QtGui
from Qt import QtCompat
from Qt import __binding__
try:
    from shiboken import wrapInstance
except ImportError:
    from shiboken2 import wrapInstance

from tpPyUtils import fileio, string, path, python

def is_pyqt():
    """
    Returns True if the current Qt binding is PyQt
    :return: bool
    """

    return 'PyQt' in __binding__


def is_pyside():
    """
    Returns True if the current Qt binding is PySide
    :return: bool
    """

    return __binding__ == 'PySide'


def is_pyside2():
    """
    Returns True if the current Qt binding is PySide2
    :return: bool
    """

    return __binding__ == 'PySide2'


def get_ui_library():
    """
    Returns the library that is being used
    """

    try:
        import PyQt5
        qt = 'PyQt5'
    except ImportError:
        try:
            import PyQt4
            qt = 'PyQt4'
        except ImportError:
            try:
                import PySide2
                qt = 'PySide2'
            except ImportError:
                try:
                    import PySide
                    qt = 'PySide'
                except ImportError:
                    raise ImportError("No valid Gui library found!")
    return qt


def wrapinstance(ptr, base=None):
    if ptr is None:
        return None

    ptr = long(ptr)
    if globals().has_key('shiboken'):
        if base is None:
            qObj = shiboken.wrapInstance(long(ptr), QObject)
            meta_obj = qObj.metaObject()
            cls = meta_obj.className()
            super_cls = meta_obj.superClass().className()
            if hasattr(QtGui, cls):
                base = getattr(QtGui, cls)
            elif hasattr(QtGui, super_cls):
                base = getattr(QtGui, super_cls)
            else:
                base = QWidget
        try:
            return shiboken.wrapInstance(long(ptr), base)
        except:
            from PySide.shiboken import wrapInstance
            return wrapInstance(long(ptr), base)
    elif globals().has_key('sip'):
        base = QObject
        return shiboken.wrapinstance(long(ptr), base)
    else:
        print('Failed to wrap object ...')
        return None


def unwrapinstance(object):
    """
    Unwraps objects with PySide
    """

    return long(shiboken.getCppPointer(object)[0])


def ui_loader(ui_file, widget=None):
    """
    Loads GUI from .ui file
    :param ui_file: str, path to the UI file
    :param widget: parent widget
    """

    ui = QtCompat.loadUi(ui_file)
    if not widget:
        return ui
    else:
        for member in dir(ui):
            if not member.startswith('__') and member is not 'staticMetaObject':
                setattr(widget, member, getattr(ui, member))
        return ui


def create_python_qrc_file(qrc_file, py_file):

    """
    Creates a Python file from a QRC file
    :param src_file: str, QRC file name
    """

    if not os.path.isfile(qrc_file):
        return

    pyside_rcc_exe_path = 'C:\\Python27\\Lib\\site-packages\\PySide\\pyside-rcc.exe'
    # pyside_rcc_exe_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'externals', 'pyside-rcc', 'pyside-rcc.exe')
    if not os.path.isfile(pyside_rcc_exe_path):
        print('RCC_EXE_PATH_DOES_NOT_EXISTS!!!!!!!!!!!!!')
    #     pyside_rcc_exe_path = filedialogs.OpenFileDialog(
    #         title='Select pyside-rcc.exe location folder ...',
    #     )
    #     pyside_rcc_exe_path.set_directory('C:\\Python27\\Lib\\site-packages\\PySide')
    #     pyside_rcc_exe_path.set_filters('EXE files (*.exe)')
    #     pyside_rcc_exe_path = pyside_rcc_exe_path.exec_()
    # if not os.path.isfile(pyside_rcc_exe_path):
        return
    # py_out = os.path.splitext(os.path.basename(src_file))[0]+'.py'
    # py_out_path = os.path.join(os.path.dirname(src_file), py_out)
    try:
        subprocess.check_output('"{0}" -o "{1}" "{2}"'.format(pyside_rcc_exe_path, py_file, qrc_file))
    except subprocess.CalledProcessError as e:
        raise RuntimeError('command {0} returned with error (code: {1}): {2}'.format(e.cmd, e.returncode, e.output))
    if not os.path.isfile(py_file):
        return
    fileio.replace(py_file, "from PySide import QtCore", "from Qt import QtCore")


def create_qrc_file(src_paths, dst_file):

    def tree(top='.',
             filters=None,
             output_prefix=None,
             max_level=4,
             followlinks=False,
             top_info=False,
             report=True):
        # The Element of filters should be a callable object or
        # is a byte array object of regular expression pattern.
        topdown = True
        total_directories = 0
        total_files = 0

        top_fullpath = os.path.realpath(top)
        top_par_fullpath_prefix = os.path.dirname(top_fullpath)

        if top_info:
            lines = top_fullpath
        else:
            lines = ""

        if filters is None:
            _default_filter = lambda x: not x.startswith(".")
            filters = [_default_filter]

        for root, dirs, files in os.walk(top=top_fullpath, topdown=topdown, followlinks=followlinks):
            assert root != dirs

            if max_level is not None:
                cur_dir = string.strips(root, top_fullpath)
                path_levels = string.strips(cur_dir, "/").count("/")
                if path_levels > max_level:
                    continue

            total_directories += len(dirs)
            total_files += len(files)

            for filename in files:
                for _filter in filters:
                    if callable(_filter):
                        if not _filter(filename):
                            total_files -= 1
                            continue
                    elif not re.search(_filter, filename, re.UNICODE):
                        total_files -= 1
                        continue

                    if output_prefix is None:
                        cur_file_fullpath = os.path.join(top_par_fullpath_prefix, root, filename)
                    else:
                        buf = string.strips(os.path.join(root, filename), top_fullpath)
                        if output_prefix != "''":
                            cur_file_fullpath = os.path.join(output_prefix, buf.strip('/'))
                        else:
                            cur_file_fullpath = buf

                    lines = "%s%s%s" % (lines, os.linesep, cur_file_fullpath)

        lines = lines.lstrip(os.linesep)

        if report:
            report = "%d directories, %d files" % (total_directories, total_files)
            lines = "%s%s%s" % (lines, os.linesep * 2, report)

        return lines

    def scan_files(src_path="."):
        filters = ['.(png|jpg|gif)$']
        output_prefix = './'
        report = False
        lines = tree(src_path, filters=filters, output_prefix=output_prefix, report=report)

        lines = lines.split('\n')
        if "" in lines:
            lines.remove("")

        return lines

    def create_qrc_body(src_path, root_res_path, use_alias=True):

        res_folder_files = path.get_absolute_file_paths(src_path)
        lines = [os.path.relpath(f, root_res_path) for f in res_folder_files]

        if use_alias:
            buf = ['\t\t<file alias="{0}">{1}</file>\n'.format(os.path.splitext(os.path.basename(i))[0].lower().replace('-', '_'), i).replace('\\', '/') for i in lines]
        else:
            buf = ["\t\t<file>{0}</file>\n".format(i).replace('\\', '/') for i in lines]
        buf = "".join(buf)
        # buf = QRC_TPL % buf
        return buf

    # Clean existing resources files and append initial resources header text
    if dst_file:
        parent = os.path.dirname(dst_file)
        if not os.path.exists(parent):
            os.makedirs(parent)
        f = file(dst_file, "w")
        f.write('<RCC>\n')

        try:
            for res_folder in src_paths:
                res_path = os.path.dirname(res_folder)
                start_header = '\t<qresource prefix="{0}">\n'.format(os.path.basename(res_folder))
                qrc_body = create_qrc_body(res_folder, res_path)
                end_header = '\t</qresource>\n'
                res_text = start_header + qrc_body + end_header

                f = file(dst_file, 'a')
                f.write(res_text)

            # Write end header
            f = file(dst_file, "a")
            f.write('</RCC>')
            f.close()
        except RuntimeError:
            f.close()


def get_signals(class_obj):
    """
    Returns a list with all signals of a class
    :param class_obj: QObject
    """

    result = filter(lambda x: isinstance(x[1], Signal), vars(class_obj).iteritems())
    if class_obj.__base__ and class_obj.__base__ != QObject:
        result.extend(get_signals(class_obj.__base__))
    return result


def safe_delete_later(widget):
    """
    calls the deleteLater method on the given widget, but only
    in the necessary Qt environment
    :param widget: QWidget
    """

    if __binding__ in ('PySide', 'PyQt4'):
        widget.deleteLater()


def show_question(parent, title, question):
    """
    Show a question QMessageBox with the given question text
    :param question: str
    :return:
    """

    flags = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    return QMessageBox.question(parent, title, question, flags)


def show_error(parent, title, error):
    """
    Show a error QMessageBox with the given error
    :return:
    """

    return QMessageBox.critical(parent, title, error)


def show_info(parent, title, info):
    """
    Show a info QMessageBox with the given info
    :return:
    """

    return QMessageBox.information(parent, title, info)


def clear_layout(layout):
    """
    Removes all the widgets added in the given layout
    :param layout: QLayout
    """

    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clear_layout(child.layout())

    # for i in reversed(range(layout.count())):
    #     item = layout.itemAt(i)
    #     if item:
    #         w = item.widget()
    #         if w:
    #             w.setParent(None)


def image_to_clipboard(path):
    """
    Copies the image at path to the system's global clipboard
    :param path: str
    """

    image = QtGui.QImage(path)
    clipboard = QApplication.clipboard()
    clipboard.setImage(image, mode=QtGui.QClipboard.Clipboard)


def get_horizontal_separator():
    v_div_w = QWidget()
    v_div_l = QVBoxLayout()
    v_div_l.setAlignment(Qt.AlignLeft)
    v_div_l.setContentsMargins(0, 0, 0, 0)
    v_div_l.setSpacing(0)
    v_div_w.setLayout(v_div_l)
    v_div = QFrame()
    v_div.setMinimumHeight(30)
    v_div.setFrameShape(QFrame.VLine)
    v_div.setFrameShadow(QFrame.Sunken)
    v_div_l.addWidget(v_div)
    return v_div_w


def dock_window(window_class):
    try:
        cmds.deleteUI(window_class.name)
    except Exception:
        pass

    main_control = cmds.workspaceControl(window_class.name, ttc=["AttributeEditor", -1], iw=300, mw=True, wp='preferred', label=window_class.title)

    control_widget = OpenMayaUI.MQtUtil.findControl(window_class.name)
    control_wrap = wrapInstance(long(control_widget), QWidget)
    control_wrap.setAttribute(Qt.WA_DeleteOnClose)
    win = window_class(control_wrap)

    cmds.evalDeferred(lambda *args: cmds.workspaceControl(main_control, e=True, rs=True))

    return win.run()


def get_rounded_mask(width, height, radius_tl=10, radius_tr=10, radius_bl=10, radius_br=10):
    region = QtGui.QRegion(0, 0, width, height, QtGui.QRegion.Rectangle)

    # top left
    round = QtGui.QRegion(0, 0, 2*radius_tl, 2 * radius_tl, QtGui.QRegion.Ellipse)
    corner = QtGui.QRegion(0, 0, radius_tl, radius_tl, QtGui.QRegion.Rectangle)
    region = region.subtracted(corner.subtracted(round))

    # top right
    round = QtGui.QRegion(width - 2 * radius_tr, 0, 2 * radius_tr, 2 * radius_tr, QtGui.QRegion.Ellipse)
    corner = QtGui.QRegion(width - radius_tr, 0, radius_tr, radius_tr, QtGui.QRegion.Rectangle)
    region = region.subtracted(corner.subtracted(round))

    # bottom right
    round = QtGui.QRegion(width - 2 * radius_br, height-2*radius_br, 2 * radius_br, 2 * radius_br, QtGui.QRegion.Ellipse)
    corner = QtGui.QRegion(width - radius_br, height-radius_br, radius_br, radius_br, QtGui.QRegion.Rectangle)
    region = region.subtracted(corner.subtracted(round))

    # bottom left
    round = QtGui.QRegion(0, height - 2 * radius_bl, 2 * radius_bl, 2 * radius_br, QtGui.QRegion.Ellipse)
    corner = QtGui.QRegion(0, height - radius_bl, radius_bl, radius_bl, QtGui.QRegion.Rectangle)
    region = region.subtracted(corner.subtracted(round))

    return region


def distance_point_to_line(p, v0, v1):
    v = QtGui.QVector2D(v1 - v0)
    w = QtGui.QVector2D(p - v0)
    c1 = QtGui.QVector2D.dotProduct(w, v)
    c2 = QtGui.QVector2D.dotProduct(v, v)
    b = c1 * 1.0 / c2
    pb = v0 + v.toPointF() * b
    return QtGui.QVector2D(p - pb).length()


def qhash (inputstr):
    instr = ""
    if isinstance (inputstr, str):
        instr = inputstr
    elif isinstance (inputstr, unicode):
        instr = inputstr.encode ("utf8")
    else:
        return -1

    h = 0x00000000
    for i in range (0, len (instr)):
        h = (h << 4) + ord(instr[i])
        h ^= (h & 0xf0000000) >> 23
        h &= 0x0fffffff
    return h


def get_focus_widget():
    """
    Gets the currently focused widget
    :return: variant, QWidget || None
    """

    return QApplication.focusWidget()


def get_widget_at_mouse():
    """
    Get the widget under the mouse
    :return: variant, QWidget || None
    """

    current_pos = QtGui.QCursor().pos()
    widget = QApplication.widgetAt(current_pos)
    return widget


def is_valid_widget(widget):
    """
    Checks if a widget is a valid in the backend
    :param widget: QWidget
    :return: bool, True if the widget still has a C++ object, False otherwise
    """

    if widget is None:
        return False

    # Added try because Houdini does not includes Shiboken library by default
    # TODO: When Houdini app class implemented, add cleaner way
    try:
        if not shiboken.isValid(widget):
            return False
    except:
        return True

    return True


def close_and_cleanup(widget):
    """
    Call close and deleteLater on a widget safely
    NOTE: Skips the close call if the widget is already not visible
    :param widget: QWidget, widget to delete and close
    """
    if is_valid_widget(widget):
        if widget.isVisible():
            widget.close()
        widget.deleteLater()


def get_string_input(message, title='Rename', parent=None, old_name=None):
    """
    Shows a Input dialog to allow the user to input a new string
    :param message: str, mesage to show in the dialog
    :param title: str, title of the input dialog
    :param parent: QWidget (optional), parent widget for the input
    :param old_name: str (optional): old name where are trying to rename
    :return: str, new name
    """

    parent = None

    dialog = QInputDialog()
    flags = dialog.windowFlags() ^ Qt.WindowContextHelpButtonHint | Qt.WindowStaysOnTopHint

    if not old_name:
        comment, ok = dialog.getText(parent, title, message, flags=flags)
    else:
        comment, ok = dialog.getText(parent, title, message, text=old_name, flags=flags)

    comment = comment.replace('\\', '_')

    if ok:
        return str(comment)


def get_comment(text_message='Add Comment', title='Save', comment_text='', parent=None):
    """
    Shows a comment dialog to allow user to input a new comment
    :param parent: QwWidget
    :param text_message: str, text to show before message input
    :param title: str, title of message dialog
    :param comment_text: str, default text for the commment
    :return: str, input comment write by the user
    """

    comment_dialog = QInputDialog()
    flags = comment_dialog.windowFlags() ^ Qt.WindowContextHelpButtonHint | Qt.WindowStaysOnTopHint
    comment, ok = comment_dialog.getText(parent, title, text_message, flags=flags, text=comment_text)
    if ok:
        return comment


def get_file(directory, parent=None):
    """
    Show a open file dialog
    :param directory: str, root directory
    :param parent: QWidget
    :return: str, selected folder or None if no folder is selected
    """

    file_dialog = QFileDialog(parent)
    if directory:
        file_dialog.setDirectory(directory)
    directory = file_dialog.getOpenFileName()
    directory = python.force_list(directory)
    if directory:
        return directory


def get_folder(directory, parent=None):
    """
    Shows a open folder dialog
    :param directory: str, root directory
    :param parent: QWidget
    :return: str, selected folder or None if no folder is selected
    """

    file_dialog = QFileDialog(parent)
    if directory:
        file_dialog.setDirectory(directory)
    directory = file_dialog.getExistingDirectory()
    if directory:
        return directory


def get_permission(message=None, cancel=True, title='Permission', parent=None):
    """
    Shows a permission message box
    :param message: str, message to show to the user
    :param cancel: bool, Whether the user can cancel the operation or not
    :param title: str, title of the window
    :param parent: QWidget
    :return: bool
    """

    message_box = QMessageBox()
    message_box.setWindowTitle(title)
    flags = message_box.windowFlags() ^ Qt.WindowContextHelpButtonHint | Qt.WindowStaysOnTopHint
    if message:
        message_box.setText(message)
    if cancel:
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
    else:
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    message_box.setWindowFlags(flags)
    result = message_box.exec_()

    if result == QMessageBox.Yes:
        return True
    elif result == QMessageBox.No:
        return False

    return None


def get_save_permission(message, file_path=None, title='Permission', parent=None):
    """
    Shows a save path message box
    :param message: str, message to show to the user
    :param file_path: str, path you want to save
    :param title: str, title of the window
    :param parent: QWidget
    :return: bool
    """

    message_box = QMessageBox()
    message_box.setWindowTitle(title)
    flags = message_box.windowFlags() ^ Qt.WindowContextHelpButtonHint | Qt.WindowStaysOnTopHint
    if file_path:
        path_message = 'Path: {}'.format(file_path)
        message_box.setInformativeText(path_message)
    message_box.setWindowFlags(flags)
    save = message_box.addButton('Save', QMessageBox.YesRole)
    no_save = message_box.addButton('Do not save', QMessageBox.NoRole)
    cancel = message_box.addButton('Cancel', QMessageBox.RejectRole)
    message_box.exec_()

    if message_box.clickedButton() == save:
        return True
    elif message_box.clickedButton() == no_save:
        return False

    return None


def get_line_layout(title, parent, *widgets):
    """
    Returns a QHBoxLayout with all given widgets added to it
    :param parent: QWidget
    :param title: str
    :param widgets: list<QWidget>
    :return: QHBoxLayout
    """

    layout = QHBoxLayout()
    layout.setContentsMargins(1, 1, 1, 1)
    if title and title != '':
        label = QLabel(title, parent)
        layout.addWidget(label)
    for w in widgets:
        if isinstance(w, QWidget):
            layout.addWidget(w)
        elif isinstance(w, QLayout):
            layout.addLayout(w)

    return layout


def get_column_layout(parent, *widgets):
    """
    Returns a QVBoxLayout with all given widgets added to it
    :param parent: QWidget
    :param widgets: list<QWidget>
    :return: QVBoxLayout
    """

    layout = QVBoxLayout()
    for w in widgets:
        if isinstance(w, QWidget):
            layout.addWidget(w)
        elif isinstance(w, QLayout):
            layout.addLayout(w)

    return layout
