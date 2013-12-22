#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Jon Surrell
# Copyright (c) 2013 Jon Surrell
#
# License: MIT
#

"""This module exports the Ghc plugin class."""

from SublimeLinter.lint import Linter, util


class Ghc(Linter):

    """Provides an interface to ghc."""

    syntax = ''
    cmd = 'ghc'
    executable = None
    regex = r''
    multiline = False
    line_col_base = (1, 1)
    tempfile_suffix = None
    error_stream = util.STREAM_STDOUT
    selectors = {}
    word_re = None
    defaults = {}
    inline_settings = None
    inline_overrides = None
    comment_re = None
