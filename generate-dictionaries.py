#!/usr/bin/env python3

import sys
import latexmap
import glob
import os
import os.path

from latexmap import mapping
mapping['~'] = ' '

print('Generating dictionaries')

# Regular expressions don't work really, but we replace a single string anyways
unicode_to_latex_mapping = {}
for token, replacement in mapping.items():
    unicode_to_latex_mapping[replacement] = "{%s}" % token

def unicode_to_latex(string):
    string = str(string)
    for char, replacement in unicode_to_latex_mapping.items():
        string = string.replace(char, replacement)

    # The returned string may still contain unicode characters if
    # the user is using xelatex. But in that case, the remapping is not
    # needed anyway.
    # However, it could also mean that the mapping needs to be updated.
    try:
        string.encode('ascii')
    except UnicodeEncodeError:
        global warned_mapping
        if not warned_mapping:
            warned_mapping = True
            log.warn(_("Generated string for LaTeX contains unicode characters. This is likely fine!"))
    return string


dest_dir = sys.argv[1]
dicts = {}

for infile in glob.glob('dict/*.ini'):
    for line in open(infile).readlines():
        if line.startswith('tex-language='):
            name = line.strip()[13:]
            if name.startswith('"'):
                assert name.endwith('"')
                name = name[1:-1]
            break
    else:
        raise AssertionError("tex-language not found in dictonary")
    assert name not in dicts
    dicts[name] = infile

for name, infile in dicts.items():
    print(f'Generating dictionary {name}')

    out = os.path.join(dest_dir, 'translator-sdaps-dictionary-%s.dict' % name)
    f = open(out, 'w')

    f.write('% This file is auto-generated from weblate translations.\n')
    f.write('% The header of the original file follows for reference:\n')
    f.write('%\n')
    header = False
    for line in open(infile).readlines():
        if line.startswith('#'):
            f.write('%' + line[1:])
            continue
        if not line.strip():
            f.write('\n')
            continue

        if not header:
            f.write('\\ProvidesDictionary{translator-sdaps-dictionary}{%s}\n\n' % name)
            header = True

        # Should be of format key="value" (also accept without quotes)
        key, value = line.strip().split('=', 1)
        if value.startswith('"'):
            assert value.endswih('"')
            value = value[1:-1]

        if key != 'tex-language':
            f.write('\\providetranslation{%s}{%s}\n' % (key, value))


