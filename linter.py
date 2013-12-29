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

    syntax = ('haskell', 'haskell-sublimehaskell', 'literate haskell')
    cmd = ('ghc', '-fno-code', '-Wall', '-Wwarn', '-fno-helpful-errors')
    regex = r'^.+:(?P<line>\d+):(?P<col>\d+):\s+(?P<warning>Warning:\s+)?(?P<message>.+)$'
    multiline = True

    # No stdin
    tempfile_suffix = {
        'haskell': 'hs',
        'haskell-sublimehaskell': 'hs',
        'literate haskell': 'lhs'}

    # ghc writes errors to STDERR
    error_stream = util.STREAM_STDERR
