# -*- coding: utf-8 -*-

"""
Here's a stand-alone logger class to help me write good output to the terminal.
"""

from __future__ import print_function
import time
import sys

__author__ = "Jakrin Juangbhanich"
__copyright__ = "Copyright 2018, Jakrin Juangbhanich"
__email__ = "juangbhanich.k@gmail.com"


class Logger:

    # Character constants (tab, ruler, etc).
    INDENT_CHAR = "   "
    RULER_CHAR = "-"
    BLANK_TAG = "   "

    # Color definitions.
    RED = '\33[31m'
    GREEN = '\33[32m'
    YELLOW = '\33[33m'
    BLUE = '\33[34m'
    BOLD = '\33[5m'
    DEFAULT_COLOR = '\33[0m'

    # Singleton instance.
    _INSTANCE = None

    # ==================================================================================================================
    # Public Interface -------------------------------------------------------------------------------------------------
    # ==================================================================================================================

    @staticmethod
    def get_instance():
        if Logger._INSTANCE is None:
            Logger()
        return Logger._INSTANCE

    @staticmethod
    def log(message, error=False):
        """ Logs a normal message at the indent level, with a timestamp. """
        Logger.get_instance()._log(message, Logger.DEFAULT_COLOR, error=error)

    @staticmethod
    def log_special(message):
        """ Logs a special (colored) message at the indent level. """
        Logger.get_instance()._log(message, Logger.GREEN)

    @staticmethod
    def log_header(message):
        """ Logs a special (colored) message at the indent level. """
        Logger.get_instance()._log(message, Logger.YELLOW)

    @staticmethod
    def log_field(field_name, value):
        """ Logs a special (colored) message at the indent level. """
        Logger.get_instance()._log_field(field_name, value)

    @staticmethod
    def log_field_red(field_name, value):
        """ Logs a special (colored) message at the indent level. """
        Logger.get_instance()._log_field(field_name, value, True)

    @staticmethod
    def log_special_break(message):
        """ Creates a line break, resets the indent level, and logs a special message. """
        Logger.line_break()
        Logger.log_special(message)

    @staticmethod
    def log_error(message):
        """ Log to the stderr stream. """
        Logger.log(message, error=True)

    @staticmethod
    def line_break(error=False):
        """ Create a horizontal line break. """
        Logger.clear_indent()
        Logger.log("", error)

    @staticmethod
    def line_break_error():
        """ Create a horizontal line break in the stderr stream. """
        Logger.line_break(error=True)

    @staticmethod
    def ruler(length=60):
        """ Creates a ruler of length n, with two line-breaks around it. """
        Logger.line_break()
        Logger.get_instance()._log(Logger.RULER_CHAR * length,
                                   color=Logger.BLUE)
        Logger.line_break()

    @staticmethod
    def ruler_error(length=60):
        """ Creates a ruler of length n, with two line-breaks around it, to the stderr stream. """
        Logger.line_break(error=True)
        Logger.get_instance()._log(Logger.RULER_CHAR * length,
                                   color=Logger.BLUE,
                                   error=True)
        Logger.line_break(error=True)

    @staticmethod
    def indent():
        """ Increase the current indent level by 1. """
        Logger.get_instance()._indent_level += 1

    @staticmethod
    def unindent():
        """ Decrease the current indent level by 1. """
        Logger.get_instance()._indent_level = \
            max(0, Logger.get_instance()._indent_level - 1)

    @staticmethod
    def clear_indent():
        """ Reset the indent level back to 0. """
        Logger.get_instance()._indent_level = 0

    # ==================================================================================================================
    # Private Methods --------------------------------------------------------------------------------------------------
    # ==================================================================================================================

    def __init__(self):
        self._indent_level = 0
        Logger._INSTANCE = self

    def _log_field(self, field_name, value, red=False):
        field_name = self._set_color("{}:".format(field_name), Logger.BLUE)
        if red:
            value = self._set_color(str(value), Logger.RED)
        message = "{} {}".format(field_name, value)
        self._print(self._add_format(message), False)

    def _log(self, message, color, error=False):
        message = self._set_color(message, color)
        self._print(self._add_format(message), error)

    def _add_format(self, message):
        message = self._indent_level * self.INDENT_CHAR + message
        output = self._get_header() + message
        return output

    def _get_header(self):
        header = "{} | ".format(self._get_readable_time(time.localtime()))
        header = self._set_color(header, self.BLUE)
        return header

    def _get_readable_time(self, time_object):
        day = self._pre_fill(time_object.tm_mday)
        date_str = "{}/{}".format(day, time_object.tm_mon)
        hour = self._pre_fill(time_object.tm_hour)
        minute = self._pre_fill(time_object.tm_min)
        time_str = "{}:{}".format(hour, minute)
        final_str = " {} {} ".format(date_str, time_str)
        return final_str

    def _set_color(self, text, color):
        return color + text + self.DEFAULT_COLOR

    @staticmethod
    def _print(message, error=False):
        if error:
            print(message, file=sys.stderr)
            sys.stderr.flush()
        else:
            print(message)
            sys.stdout.flush()

    @staticmethod
    def _pre_fill(string, length=2, char='0'):
        string = str(string)
        while len(string) < length:
            string = char + string
        return string
