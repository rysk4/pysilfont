# Changelog

## [1.6.1] - - Placeholder for next release


### Added

| Command                                            | Description                                                                                   |
|----------------------------------------------------|-----------------------------------------------------------------------------------------------|
| [psfcheckproject](docs/scripts.md#psfcheckproject) | Check UFOs in designspace files have consistent glyph inventory & unicode values (1.6.1.dev2) |

### Changed

check&fix, used by most UFO commands, no longer warns if styleMapFamilyName or styleMapStyleName
are missing in fontinfo (1.6.1.dev1)\
Low-level bug fix to ufo.py found when running some temp code! Not previously found in live code. (1.6.1.dev1)

### Removed

None

## [1.6.0] - 2022-07-25 Maintenance Release - general updates

General updates over the last two years, adding new scripts and updating existing in response to new
needs or to adjust for changes to third-party software.

### Added

| Command | Description |
| ------- | ----------- |
| [psfcheckclassorders](docs/scripts.md#psfcheckclassorders) | Verify classes defined in xml have correct ordering where needed |
| [psfcheckftml](docs/scripts.md#psfcheckftml) | Check ftml files for structural integrity |
| [psfcheckglyphinventory](docs/scripts.md#psfcheckglyphinventory) | Warn for differences in glyph inventory and encoding between UFO and input file (e.g., glyph_data.csv) |
| [psfcheckinterpolatable](docs/scripts.md#psfcheckinterpolatable) | Check UFOs in a designspace file are compatible with interpolation |
| [psffixfontlab](docs/scripts.md#psffixfontlab) | Make changes needed to a UFO following processing by FontLab |
| [psfsetdummydsig](docs/scripts.md#psfsetdummydsig) | Add a dummy DSIG table into a TTF font |
| [psfsetglyphdata](docs/scripts.md#psfsetglyphdata) | Update and/or sort glyph_data.csv based on input file(s) |
| [psfshownames](docs/scripts.md#psfshownames) | Display name fields and other bits for linking fonts into families |
| [psfwoffit](docs/scripts.md#psfwoffit) | Convert between ttf, woff, and woff2 |

### Changed

Multiple changes!

### Removed

None

## [1.5.0] - 2020-05-20 - Maintenance Release; Python 2 support removed

Added support for Font Bakery to make it simple for projects to run a standard set ot checks designed to fit in 
with [Font Development Best Practices](https://silnrsi.github.io/FDBP/en-US/index.html).

Improvements to feax support

Many other updates

### Added

| Command | Description |
| ------- | ----------- |
| [psfftml2TThtml](docs/scripts.md#psfftml2TThtml) | Convert FTML document to html and fonts for testing TypeTuner |
| [psfmakescaledshifted](docs/scripts.md#psfmakescaledshifted) | Creates scaled and shifted versions of glyphs |
| [psfrunfbchecks](docs/scripts.md#psfrunfbchecks) | Run Font Bakery checks using a standard profile with option to specify an alternative profile |
| [psfsetdummydsig](docs/scripts.md#psfsetdummydsig) | Put a dummy DSIG table into a TTF font |

### Changed

Multiple minor changes and bug fixes

### Removed

None

## [1.4.2] - 2019-07-30 - Maintenance release

Updated the execute() framework used by scripts to add support for opening fonts with fontParts and remove support for opening fonts with FontForge.

Updates to normalization and check&fix to work better with FontForge-based workflows

Improvements to command-line help to display info on params and default values

Improvements to log file creation, including logs, by default, going to a logs sub-directory

Some changes are detailed below, but check commit logs for full details.

### Added

| Command | Description |
| ------- | ----------- |
| [psfbuildcompgc](docs/scripts.md#psfbuildcompgc) | Add composite glyphs to UFO using glyphConstruction based on a CD file |
| [psfdeflang](docs/scripts.md#psfdeflang) | Changes default language behaviour in a font |
| [psfdupglyphs](docs/scripts.md#psfdupglyphs) | Duplicates glyphs in a UFO based on a csv definition |
| [psfexportmarkcolors](docs/scripts.md#psfexportmarkcolors) | Export csv of mark colors |
| [psffixffglifs](docs/scripts.md#psffixffglifs) | Make changes needed to a UFO following processing by FontForge |
| [psfgetglyphnames](docs/scripts.md#psfgetglyphnames) | Create a file of glyphs to import from a list of characters to import |
| [psfmakedeprecated](docs/scripts.md#psfmakedeprecated) | Creates deprecated versions of glyphs |
| [psfsetmarkcolors](docs/scripts.md#psfsetmarkcolors) | Set mark colors based on csv file |
| [psftuneraliases](docs/scripts.md#psftuneraliases) | Merge alias information into TypeTuner feature xml file |

### Changed

Multiple minor changes and bug fixes

### Removed

The following scripts moved from installed scripts to examples

- ffchangeglyphnames
- ffcopyglyphs
- ffremovealloverlaps

## [1.4.1] - 2019-03-04 - Maintenance release

Nearly all scripts should work under Python 2 & 3

**Future work will be tested just with Python 3** but most may still work with Python 2.

Some changes are detailed below, but check commit logs for full details.

### Added

psfversion - Report version info for pysilfont, python and various dependencies
psfufo2gylphs - Creates a .gypyhs file from UFOs using glyphsLib

### Changed

psfremovegliflibkeys now has -b option to remove keys beginning with specified string

psfglyphs2ufo updated to match new psfufo2glyphs.  Now has -r to restore specific keys

Many changes to .fea support

The pytest-based test setup has been expanded and refined

### Removed

Some scripts moved from installed scripts to examples

## [1.4.0] - 2018-10-03 - Python 2+3 support

### Added

### Changed

Libraries and most installed scripts updated to work with Python 2 and python 3

All scripts should work as before under Python 2, but a few scripts need further work to run under Python 3:
- All ff* scripts
- psfaddanchors
- psfcsv2comp
- psfexpandstroke
- psfsubset

The following scripts have not been fully tested with the new libraries
- psfchangegdlnames
- psfcompdef2xml
- psfcopymeta
- psfexportpsnames
- psfftml2odt
- psfremovegliflibkeys
- psfsetversion
- psfsyncmeta
- psftoneletters
- psfxml2compdef

### Removed

## [1.3.1] - 2018-09-27 - Stable release prior to Python 2+3 merge

### Added
- psfcopyglyphs
- psfcreateinstances
- psfcsv2comp
- psfmakefea
- psfremovegliflibkeys
- psfsetkeys
- psfsubset

Regression testing framework

### Changed

(Changes not documented here)

### Removed


## [1.3.0] - 2018-04-25 - First versioned release
