# Python_HeidelTime
This projects implements a Python Wrapper for the temporal tagger [HeidelTime](https://github.com/HeidelTime/heideltime). To achieve that, it makes use of the HeidelTime-standalone application. We only tested this code for Debian-based systems and cannot guarantee functionality for other systems.


## Installation
To use Python_HeidelTime, it is necessary to install HeidelTime-standalone first. A current download can be found on their [releases page](https://github.com/HeidelTime/heideltime/releases). At the point of the development of this project, version 2.2.1 was the most current one. Support for newer or older versions is not guaranteed. A detailed description of the installation process is found in the [HeidelTime Standalone Manual](https://gate.ac.uk/gate/plugins/Tagger_GATE-Time/doc/HeidelTime-Standalone-Manual.pdf)

For convenience we also provide you with a installation script for HeidelTime-standalone that does everything (including changing the appropriate config files) for you. Just type the following into your console:
```
chmod +x install_heideltime_standalone.sh
./install_heideltime_standalone.sh
```


### MacOS Installation
If your operating system is Mac OSX, you need to download an appropriate treetagger for your OS. Replace line 15 in `install_heideltime_standalone.sh` with 
```bash
wget --no-verbose https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tree-tagger-MacOSX-3.2.2.tar.gz
```
You then need to manually set the path to the treetagger in `config.props` for the HeidelTime-standalone installation.
Do not move the files after the installation; HeidelTime requires absolute paths in its config files.


### Further Configurations
In the ```config.props``` file of HeidelTime, you can also specify if you want to limit HeidelTime to detect only Timex3 expressions of certain types (data, duration, set, and time).

If you do not want to use this script, you need to install HeidelTime-standalone yourself. Additionally, it is necessary to specify the installation directory of HeidelTime-standalone in the config_Heideltime.py. Please notice that the path to HeidelTime-standalone has to specified as a string object.`  
For system wide usage a `setup.py` is provided that installs python_heideltime as a package. It can be used for installation by:
```
python3 -m pip install .
```

When using Python_HeidelTime, please also cite HeidelTime itself as stated on their [project page](https://github.com/HeidelTime/heideltime).



## Usage
The main class of Python_HeidelTime is simply called Heideltime and is initialized without any parameters.
All paramaters x can be specified by the set_x methods. Typically, they are named as described in the [HeidelTime Standalone Manual](https://gate.ac.uk/gate/plugins/Tagger_GATE-Time/doc/HeidelTime-Standalone-Manual.pdf). The correct use of all parameters is also given in the manual. When certain parameters are renamed, it is stated so in the source code.

After initialization, a text can be parsed by the parse function by passing the argument as a string object.

The following code snippet works a simple example.

```python
from python_heideltime import Heideltime

heideltime_parser = Heideltime()
heideltime_parser.set_document_type('NEWS')
print(heideltime_parser.parse('Yesterday, I bought a cat! It was born earlier this year.'))
```

Which should result in the following output (with regard to your current date).

```
<?xml version="1.0"?>
<!DOCTYPE TimeML SYSTEM "TimeML.dtd">
<TimeML>
<TIMEX3 tid="t1" type="DATE" value="2019-06-13">Yesterday</TIMEX3>, I bought a cat! It was born <TIMEX3 tid="t3" type="DATE" value="2019" mod="START">earlier this year</TIMEX3>.
</TimeML>
```
