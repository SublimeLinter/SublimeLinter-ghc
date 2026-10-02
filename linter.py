import json

from SublimeLinter.lint import Linter, LintMatch, util


TAB_STOP = 8


class Ghc(Linter):
    # `-fdiagnostics-as-json` needs GHC 9.10 or newer. `-v0` stops ghc from
    # writing its progress lines to stdout, which is not a usable handle for
    # a Windows GUI program.
    cmd = ('ghc', '-v0', '-fno-code', '-Wall', '-Wwarn',
           '-fdiagnostics-as-json', '$temp_file')
    regex = None
    defaults = {
        'selector': 'source.haskell, text.tex.latex.haskell'
    }

    tempfile_suffix = {
        'haskell': 'hs',
        'haskell-sublimehaskell': 'hs',
        'literate haskell': 'lhs',
        'literatehaskellbirdstyle': 'lhs'
    }

    # ghc writes the diagnostics to STDERR. Ask for both streams so that
    # SublimeLinter pipes stdout as well.
    error_stream = util.STREAM_BOTH

    def parse_output(self, proc, virtual_view):
        unparsed = []
        found = False
        for line in proc.stderr.splitlines():
            line = line.strip()
            if not line:
                continue

            try:
                item = json.loads(line)
            except ValueError:
                unparsed.append(line)
                continue

            if not isinstance(item, dict):
                unparsed.append(line)
                continue

            found = True
            error = self.process_match(self.to_match(item), virtual_view)
            if error:
                yield error

        if unparsed:
            output = '\n'.join(unparsed)
            if found:
                self.logger.info(
                    '{}: ignoring non-JSON output:\n{}'.format(self.name, output)
                )
            else:
                # E.g. a ghc older than 9.10 does not know the JSON flag.
                self.on_stderr(output)

    def to_match(self, item):
        span = item.get('span')
        if span:
            filename = span['file']
            line = span['start']['line'] - 1
            col = span['start']['column'] - 1
            end_line = span['end']['line'] - 1
            end_col = span['end']['column'] - 1
        else:
            filename = None
            line = col = 0
            end_line = end_col = None

        code = item.get('code')
        message = '\n'.join(item.get('message') or []).strip()
        for hint in item.get('hints') or []:
            message += '\n' + hint
        flags = (item.get('reason') or {}).get('flags') or []
        if flags:
            message += ' ' + ' '.join('[-W{}]'.format(flag) for flag in flags)

        return LintMatch(
            match=item,
            filename=filename,
            line=line,
            col=col,
            end_line=end_line,
            end_col=end_col,
            error_type='error' if item.get('severity') == 'Error' else 'warning',
            code=None if code is None else 'GHC-{}'.format(code),
            message=message,
        )

    def convert_column(self, line, col, m, vv):
        # ghc counts characters, except that a tab advances the column to the
        # next multiple of `TAB_STOP`. Translate that back to a character index.
        text = vv.select_line(line)
        visual = 0
        for index, char in enumerate(text):
            if visual >= col:
                return index
            visual = (visual // TAB_STOP + 1) * TAB_STOP if char == '\t' else visual + 1
        return len(text) + (col - visual)
