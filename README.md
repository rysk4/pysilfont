# Pysilfont - a collection of utilities for font development

Pysilfont is a collection of tools to support font development, with an emphasis on UFO-based workflows. With some limitations, all UFO scripts in Pysilfont should work with UFO2 or UFO3 source files - and can convert from one format to the other.

In addition, all scripts will output UFOs in a normalized form, designed to work with source control systems.

Please read the main [documentation](docs/docs.md) in the docs folder for more details. Within there is a list of [scripts](docs/scripts.md).

## Installation

Pysilfont requires Python 3.6+ and pip3. Some scripts also need other libraries.

### Simple install
To just install the main scripts without cloning the github repository run:
```
sudo python3 -m pip install git+https://github.com/silnrsi/pysilfont
```

This will allow you to run the scripts listed in [scripts.md](docs/scripts.md), but won’t give access
to the example scripts or give you the code locally to look at.

### Full install

First clone this repository or download the files from this [github URL](https://github.com/silnrsi/pysilfont). 
Then navigate to the resulting pysilfont directory and run:
```
sudo python3 -m pip install .
```
in the pysilfont directory

### Uninstalling pysilfont

pip3 can be used to uninstall pysilfont:
```
sudo pip3 uninstall pysilfont
```

## Contributing to the project

Pysilfont is developed and maintained by SIL International’s [Writing Systems Technology team ](https://software.sil.org/wstech/), though contributions from anyone are welcome. Pysilfont is copyright (c) 2014-2022 [SIL International](http://www.sil.org) and licensed under the [MIT license](http://en.wikipedia.org/wiki/MIT_License). The project is hosted at [https://github.com/silnrsi/pysilfont](https://github.com/silnrsi/pysilfont).
