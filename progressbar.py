#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright: 2009 Nadia Alramli
# License: BSD
#
# Modified by Alexis GRIMALDI

"""Draws an animated terminal progress bar
Usage:
    p = ProgressBar("blue")
    p.render(percentage, message)
"""

from terminal import terminal
import sys


class ProgressBar(object):
    """Terminal progress bar class"""
    TEMPLATE = (
        '%(premessage)s\n\n%(percent)-2s%% %(color)s%(progress)s%(normal)s%(empty)s %(message)s\n'
    )
    PADDING = 7

    def __init__(self, color=None, width=None, block='█', empty=' '):
        """
        color -- color name (BLUE GREEN CYAN RED MAGENTA YELLOW WHITE BLACK)
        width -- bar width (optinal)
        block -- progress display character (default '█')
        empty -- bar display character (default ' ')
        """
        if color:
            self.color = getattr(terminal, color.upper())
        else:
            self.color = ''
        if width and width < terminal.COLUMNS - self.PADDING:
            self.width = width
        else:
            # Adjust to the width of the terminal
            self.width = terminal.COLUMNS - self.PADDING
        self.block = block
        self.empty = empty
        self.progress = None
        self.lines = 0

    def render(self, percent, message='', premessage=''):
        """Print the progress bar
        percent -- the progress percentage %
        message -- message string (optional)
        premessage -- message string above the progress bar (optional)
        """
        inline_msg_len = 0
        if message:
            # The length of the first line in the message
            inline_msg_len = len(message.splitlines()[0])
        if inline_msg_len + self.width + self.PADDING > terminal.COLUMNS:
            # The message is too long to fit in one line.
            # Adjust the bar width to fit.
            bar_width = terminal.COLUMNS - inline_msg_len - self.PADDING
        else:
            bar_width = self.width

        # Check if render is called for the first time
        if self.progress is not None:
            self.clear()
        self.progress = (bar_width * percent) / 100
        data = self.TEMPLATE % {
            'premessage': premessage,
            'percent': percent,
            'color': self.color,
            'progress': self.block * self.progress,
            'normal': terminal.NORMAL,
            'empty': self.empty * (bar_width - self.progress),
            'message': message
        }
        sys.stdout.write(data)
        sys.stdout.flush()
        # The number of lines printed
        self.lines = len(data.splitlines())

    def clear(self):
        """Clear all printed lines"""
        sys.stdout.write(
            self.lines * (terminal.UP + terminal.BOL + terminal.CLEAR_EOL)
        )
