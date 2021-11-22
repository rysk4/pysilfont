#!/usr/bin/env python
__doc__ = '''Reads a designSpace file and create a Glyphs file from its linked ufos'''
__url__ = 'http://github.com/silnrsi/pysilfont'
__copyright__ = 'Copyright (c) 2018 SIL International (http://www.sil.org)'
__license__ = 'Released under the MIT License (http://opensource.org/licenses/MIT)'
__author__ = 'David Raymond'

from silfont.core import execute, splitfn

from glyphsLib import to_glyphs
from fontTools.designspaceLib import DesignSpaceDocument
import os

argspec = [
    ('designspace', {'help': 'Input designSpace file'}, {'type': 'filename'}),
    ('glyphsfile', {'help': 'Output glyphs file name', 'nargs': '?' }, {'type': 'filename', 'def': None}),
    ('--no_preserve_glyphsapp_metadata', {'help': "Don't store some glyphs data in lib.plist" , 'action': 'store_true', 'default': False}, {}),
    ('--glyphsformat', {'help': "Format for glyphs file (2 or 3)", 'default': "2"}, {}),

    #    ('--nofixes', {'help': 'Bypass code fixing data', 'action': 'store_true', 'default': False}, {}),
    ('-l', '--log', {'help': 'Log file'}, {'type': 'outfile', 'def': '_ufo2glyphs.log'})]

# This is just bare-bones code at present so does the same as glyphsLib's ufo2glyphs!
# It is designed so that data could be massaged, if necessary, on the way.  No such need has been found so far

def doit(args):
    glyphsfile = args.glyphsfile
    logger = args.logger
    gformat = args.glyphsformat
    if gformat in ("2","3"):
        gformat = int(gformat)
    else:
        logger.log("--glyphsformat must be 2 or 3", 'S')
    if glyphsfile is None:
        (path,base,ext) = splitfn(args.designspace)
        glyphsfile = os.path.join(path, base + ".glyphs" )
    else:
        (path, base, ext) = splitfn(glyphsfile)
    backupname = os.path.join(path, base + "-backup.glyphs" )
    logger.log("Opening designSpace file", "I")
    ds = DesignSpaceDocument()
    ds.read(args.designspace)
    logger.log("Now creating glyphs object", "I")
    glyphsfont = to_glyphs(ds, minimize_ufo_diffs=not(args.no_preserve_glyphsapp_metadata))
    glyphsfont.format_version = gformat

    if os.path.exists(glyphsfile): # Create a backup
        logger.log("Renaming existing glyphs file to " + backupname, "I")
        os.renames(glyphsfile, backupname)
    logger.log("Writing glyphs file: " + glyphsfile, "I")
    glyphsfont.save(glyphsfile)

def cmd(): execute(None, doit, argspec)
if __name__ == "__main__": cmd()
