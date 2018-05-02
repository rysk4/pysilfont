#!/usr/bin/env python
'Generate instance UFOs from a designspace document and master UFOs'

# Python 2.7 script to build instance UFOs from a designspace document
# If a file is given, all instances are built
# A particular instance to build can be specified using the -i option
#  and the 'name' attribute value for an 'instance' element in the designspace file
#  Or it can be specified using the -a and -v options
#  to specify any attribute and value pair for an 'instance' in the designspace file
#  If more than one instances matches, all will be built
# A prefix for the output path can be specified (for smith processing)
# If the location of an instance UFO matches a master's location,
#  glyphs are copied instead of calculated
#  This allows instances to build with glyphs that are not interpolatable
#  An option exists to calculate glyphs instead of copying them
# If a folder is given using an option, all instances in all designspace files are built
#  Specifying an instance to build or an output path prefix is not supported with a folder
#  Also, all glyphs will be calculated

__url__ = 'http://github.com/silnrsi/pysilfont'
__copyright__ = 'Copyright (c) 2018 SIL International  (http://www.sil.org)'
__license__ = 'Released under the MIT License (http://opensource.org/licenses/MIT)'
__author__ = 'Alan Ward'

import os
from mutatorMath.ufo.document import DesignSpaceDocumentReader
from mutatorMath.ufo.instance import InstanceWriter
from fontMath.mathGlyph import MathGlyph
from mutatorMath.ufo import build as build_designspace
from silfont.core import execute

argspec = [
    ('designspace_path', {'help': 'Path to designspace document (or folder of them)'}, {}),
    ('-i', '--instanceName', {'help': 'Font name for instance to build'}, {}),
    ('-a', '--instanceAttr', {'help': 'Attribute used to specify instance to build'}, {}),
    ('-v', '--instanceVal', {'help': 'Value of attribute specifying instance to build'}, {}),
    ('-f', '--folder', {'help': 'Build all designspace files in a folder','action': 'store_true'}, {}),
    ('-o', '--output', {'help': 'Prepend path to all output paths'}, {}),
    ('--forceInterpolation', {'help': 'If an instance matches a master, calculate glyphs instead of copying them',
                               'action': 'store_true'}, {}),
    ('--roundInstances', {'help': 'Apply integer rounding to all geometry when interpolating',
                           'action': 'store_true'}, {}),
    ('-l','--log',{'help': 'Log file (default: *_createinstances.log)'}, {'type': 'outfile', 'def': '_createinstances.log'}),
]

# Class factory to wrap a subclass in a closure to store values not defined in the original class
#  that our method overrides will utilize
# The class methods will fail unless the class is generated by the factory, which is enforced by scoping
# Using class attribs or global variables would violate encapsulation even more
#  and would only allow for one instance of the class
def InstanceWriterCF(output_path_prefix, calc_glyphs):

    class LocalInstanceWriter(InstanceWriter):

        def __init__(self, path, *args, **kw):
            if output_path_prefix:
                path = os.path.join(output_path_prefix, path)
            return super(LocalInstanceWriter, self).__init__(path, *args, **kw)

        # Override the method used to calculate glyph geometry
        # If copy_glyphs is true and the glyph being processed is in the same location
        # (has all the same axes values) as a master UFO,
        # then extract the glyph geometry directly into the target glyph.
        # FYI, in the superclass method, m = buildMutator(); m.makeInstance() returns a MathGlyph
        def _calculateGlyph(self, targetGlyphObject, instanceLocationObject, glyphMasters):
            # Search for a glyphMaster with the same location as instanceLocationObject
            found = False
            if not calc_glyphs: # i.e. if copying glyphs
                for item in glyphMasters:
                    locationObject = item['location'] # mutatorMath Location
                    if locationObject.sameAs(instanceLocationObject) == 0:
                        found = True
                        fontObject = item['font'] # defcon Font
                        glyphName = item['glyphName'] # string
                        glyphObject = MathGlyph(fontObject[glyphName])
                        glyphObject.extractGlyph(targetGlyphObject, onlyGeometry=True)
                        break

            if not found: # includes case of calc_glyphs == True
                super(LocalInstanceWriter, self)._calculateGlyph(targetGlyphObject,
                                                                 instanceLocationObject,
                                                                 glyphMasters)

    return LocalInstanceWriter

logger = None
severe_error = False
def progress_func(state="update", action=None, text=None, tick=0):
    global severe_error
    if logger:
        if state == 'error':
            if str(action) == 'unicodes':
                logger.log("%s: %s\n%s" % (state, str(action), str(text)), 'W')
            else:
                logger.log("%s: %s\n%s" % (state, str(action), str(text)), 'E')
                severe_error = True
        else:
            logger.log("%s: %s\n%s" % (state, str(action), str(text)), 'I')

def doit(args):
    global logger
    logger = args.logger

    designspace_path = args.designspace_path
    instance_font_name = args.instanceName
    instance_attr = args.instanceAttr
    instance_val = args.instanceVal
    output_path_prefix = args.output
    calc_glyphs = args.forceInterpolation
    build_folder = args.folder
    round_instances = args.roundInstances

    if instance_font_name and (instance_attr or instance_val):
        args.logger.log('--instanceName is mutually exclusive with --instanceAttr or --instanceVal','S')
    if (instance_attr and not instance_val) or (instance_val and not instance_attr):
        args.logger.log('--instanceAttr and --instanceVal must be used together', 'S')
    if (build_folder and (instance_font_name or instance_attr or instance_val
                          or output_path_prefix or calc_glyphs)):
        args.logger.log('--folder cannot be used with options: -i, -a, -v, -o, --forceInterpolation', 'S')

    args.logger.log('Interpolating master UFOs from designspace', 'P')
    if not build_folder:
        if not os.path.isfile(designspace_path):
            args.logger.log('A designspace file (not a folder) is required', 'S')
        reader = DesignSpaceDocumentReader(designspace_path, ufoVersion=3,
                                           roundGeometry=round_instances,
                                           progressFunc=progress_func)
        # assignment to an internal object variable is a kludge, probably should use subclassing instead
        reader._instanceWriterClass = InstanceWriterCF(output_path_prefix, calc_glyphs)
        if calc_glyphs:
            args.logger.log('Interpolating glyphs where an instance font location matches a master', 'P')
        if instance_font_name or instance_attr:
            key_attr = instance_attr if instance_val else 'name'
            key_val = instance_val if instance_attr else instance_font_name
            reader.readInstance((key_attr, key_val))
        else:
            reader.readInstances()
    else:
        # The below uses a utility function that's part of mutatorMath
        #  It will accept a folder and processes all designspace files there
        args.logger.log('Interpolating glyphs where an instance font location matches a master', 'P')
        build_designspace(designspace_path,
                          outputUFOFormatVersion=3, roundGeometry=round_instances,
                          progressFunc=progress_func)

    if not severe_error:
        args.logger.log('Done', 'P')
    else:
        args.logger.log('Done with severe error', 'S')

def cmd(): execute(None, doit, argspec)
if __name__ == '__main__': cmd()

# Future development might use: fonttools\Lib\fontTools\designspaceLib to read
#  the designspace file (which is the most up-to-date approach)
#  then pass that object to mutatorMath, but there's no way to do that today.


# For reference:
# from mutatorMath/ufo/__init__.py:
# 	build() is a convenience function for reading and executing a designspace file.
# 		documentPath: 				filepath to the .designspace document
# 		outputUFOFormatVersion:		ufo format for output
# 		verbose:					True / False for lots or no feedback [to log file]
# 		logPath:					filepath to a log file
# 		progressFunc:				an optional callback to report progress.
# 									see mutatorMath.ufo.tokenProgressFunc
#
# class DesignSpaceDocumentReader(object):
# def __init__(self, documentPath,
#         ufoVersion,
#         roundGeometry=False,
#         verbose=False,
#         logPath=None,
#         progressFunc=None
#         ):
#
# def readInstance(self, key, makeGlyphs=True, makeKerning=True, makeInfo=True):
# def readInstances(self, makeGlyphs=True, makeKerning=True, makeInfo=True):