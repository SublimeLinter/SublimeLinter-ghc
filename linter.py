from SublimeLinter.lint import Linter, util
from os.path import basename


class Ghc(Linter):
    cmd = ('ghc', '-fno-code', '-Wall', '-Wwarn', '-fno-helpful-errors',
           '$temp_file')
    regex = (
        r'\s*(?P<filename>.+):'
        r'\s*(?P<line>\d+):(?P<col>\d+):'
        r'\s*(?:(?P<warning>[Ww]arning):|(?P<error>[Ee]rror):)?'
        r'\s*(?P<flag>\[-W[^\]]*\])?'
        r'\s*(?P<message>.+?):?$'
    )
    multiline = True
    defaults = {
        'selector': 'source.haskell, text.tex.latex.haskell'
    }

    tempfile_suffix = {
        'haskell': 'hs',
        'haskell-sublimehaskell': 'hs',
        'literate haskell': 'lhs',
        'literatehaskellbirdstyle': 'lhs'
    }

    # ghc writes errors to STDERR
    error_stream = util.STREAM_STDERR

    def split_match(self, match):
        """Override to ignore errors reported in imported files."""
        error = super().split_match(match)

        match_filename = basename(error['filename'])
        linted_filename = basename(self.context['temp_file'])
        if match_filename != linted_filename:
            return None

        if error['flag']:
            error['message'] += " " + error['flag']
        return error
