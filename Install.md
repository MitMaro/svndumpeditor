# Installation #

## Requirements ##

  * [Python](http://www.python.org/download/) 2.5+ earlier versions may work
  * [wxPython](http://www.wxpython.org/download.php) 2.8.9.2 tested, lower versions should work
  * Works with any regular Subversion dump file, ie not delta or incremental dumps

## First Run ##
### Unix like including Mac ###
Make sure you satisfy the above requirements.

  * To check your python version run `python --version` in your command line.
  * To check your wxPython version run this script:
```
import wx
print wx.__version__
```
If you get an error complaining about no module named wx then you don't have wxPython installed correctly. If there is no error you should get the version of wxPython.
  * Extract the downloaded archive.
  * From the command line `cd` into the `src` directory of the extracted archive.
  * Run `python main.py`

### Windows ###
No reason it shouldn't work, make sure you have all the requirements and run it. Someday I will install Windows and write up better instructions. Or someone else can do it :).