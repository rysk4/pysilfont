#!/usr/bin/env python
'Generate a ttf file without OpenType tables from a UFO'
__url__ = 'http://github.com/silnrsi/pysilfont'
__copyright__ = 'Copyright (c) 2017 SIL International  (http://www.sil.org)'
__license__ = 'Released under the MIT License (http://opensource.org/licenses/MIT)'
__author__ = 'Alan Ward'

# Compared to fontmake it does not decompose glyphs or remove overlaps 
# and curve conversion seems to happen in a different way.

# The easiest way to install all the needed libraries is to install fontmake.
#   [sudo] pip install fontmake
# If you want to isolate all the libraries fontmake needs,
# you can install fontmake in a virtual environment and run this script there

# TODO: rename according to pysilfont conventions

from silfont.core import execute
import defcon, ufo2ft.outlineCompiler

argspec = [
    ('iufo', {'help': 'Input UFO folder'}, {}),
    ('ottf', {'help': 'Output ttf file name'}, {})]

PUBLIC_PREFIX = 'public.'

def doit(args):
    ufo = defcon.Font(args.iufo)

#    args.logger.log('Converting UFO to ttf and compiling fea')
#    font = ufo2ft.compileTTF(ufo,
#        glyphOrder = ufo.lib.get(PUBLIC_PREFIX + 'glyphOrder'),
#        useProductionNames = False)

    args.logger.log('Converting UFO to ttf without OT', 'P')
    outlineCompiler = ufo2ft.outlineCompiler.OutlineTTFCompiler(ufo,
        glyphOrder=ufo.lib.get(PUBLIC_PREFIX + 'glyphOrder'),
        convertCubics=True)
    font = outlineCompiler.compile()

    args.logger.log('Saving ttf file', 'P')
    font.save(args.ottf)

    args.logger.log('Done', 'P')

def cmd(): execute(None, doit, argspec)
if __name__ == '__main__': cmd()
