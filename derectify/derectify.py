import os
import sys

from docopt import docopt


MODIFIER = '\u25BD'
# MODIFIER = '\u2207'

OUTPUT_EXTENSION = '.derectified'


__doc__ = '''Remove hypens and line breaks in text.

Usage:
  derectify [options] [-o OUTPUT|-O] [<input>]

Options:
  <input>       Input file. Specify `-` to read from the standard input.
  -o OUTPUT     Output file.
  -O            Set the output file name to `<input>.%s`.
  -w WIDTH      Don't concatenate lines with fewer characters than this [default: 25].
  -n            Show positions where hypens and line breaks to be removed.
''' % OUTPUT_EXTENSION


def main():
    args = docopt(__doc__)
    input_file = args['<input>'] or '-'
    output_file = args['-o'] or '-'
    autogen_output_file_name = args['-O']
    option_dry_run = args['-n']
    min_width = int(args['-w'])
    
    if input_file == '-':
        lines = sys.stdin.readlines()
    else:
        with open(input_file, 'rt') as inp:
            lines = inp.readlines()
    lines = [L.rstrip() for L in lines]

    for i, L in enumerate(lines):
        L2 = lines[i + 1] if i + 1 < len(lines) else ''
        if len(L) < min_width:
            pass
        elif L2 == '':
            pass
        elif L.endswith('.'):
            pass
        elif L.endswith('-'):
            L = L[:-1] + MODIFIER + '-'
        else:
            if not L.endswith(' '):
                L += ' ' + MODIFIER
            else:
                L += + MODIFIER
        lines[i] = L

    if autogen_output_file_name:
        if input_file == '-':
            output_file = 'a' + OUTPUT_EXTENSION
        else:
            output_file = input_file + OUTPUT_EXTENSION
    if output_file == '-':
        outp = sys.stdout
    else:
        outp = open(output_file, 'wt')
    if option_dry_run:
        print('\n'.join(lines), file=outp)
    else:
        for L in lines:
            L = L + '\n'
            p = L.find(MODIFIER)
            if p >= 0:
                L = L[:p]
            print(L, end='', file=outp)
    if outp is not sys.stdout:
        outp.close()


if __name__ == '__main__':
    main()
