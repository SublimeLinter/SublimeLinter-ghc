from SublimeLinter.lint import Linter, util
from os.path import basename


class Ghc(Linter):
    cmd = ('ghc', '-fno-code', '-Wall', '-Wwarn', '-fno-helpful-errors',
           '$temp_file')
    regex = (
        r'^(?P<filename>.+):'
        r'(?P<line>\d+):(?P<col>\d+):'
        r'\s+(?P<warning>Warning:\s+)?(?P<message>.+)$'
    )
    multiline = True
    defaults = {
        'selector': 'source.haskell, text.tex.latex.haskell'
    }

    # No stdin
    tempfile_suffix = {
        'haskell': 'hs',
        'haskell-sublimehaskell': 'hs',
        'literate haskell': 'lhs'
    }

    # ghc writes errors to STDERR
    error_stream = util.STREAM_STDERR

    def split_match(self, match):
        """Override to ignore errors reported in imported files."""
        match, line, col, error, warning, message, near = (
            super().split_match(match)
        )

        match_filename = basename(match.groupdict()['filename'])
        linted_filename = basename(self.filename)

        if match_filename != linted_filename:
            return None, None, None, None, None, '', None

        return match, line, col, error, warning, message, near
