Introduction

Scopemate.py is a Python script designed to take a screenshot of an oscilloscope, specifically the Rigol DS2000 series instruments, and store it on a PC. The main purpose of this code is to simplify the process of capturing images of the oscilloscope's screen, which can be useful for documentation, analysis, or presentation.

The main function of the script is to take a screenshot. If desired, it can additionaly be de-cluttered by masking out left and right tabs, top left corner as well as trigger frequency indicator on the right of the screen, either separately or all at once. In addition, instrument information, specifically Brand, Model, Serial number, and firmware version, as well as calibration date and time, are automatically saved in a text chunk of the screenshot image file. In addition, a comment can be provided via a command line argument. Auxiliary functions are available. See below for details.

The script takes several inputs:

* A resource identifier (instrument address) that specifies the connection details to the oscilloscope.

* An optional list of masks, which are images used to overlay on top of the screenshot filling the area(s) with black pixels.

* An optional output filename prefix, which allows the user to specify a custom name for the saved screenshot. The full filename will include the current date and time, so each captured image is uniquely labeled.

* A comment which will be written into the screenshot image file.

* Oscilloscope and PC clocks can be synchronized before taking the screenshot. Also, automatic measurement outputs at the bottom of the oscilloscope display can be turned off prior to taking the screenshot.


Installation

* (optional but highly recommended) Install and activate a virtual environment 
* Install dependencies: pip install pyvisa pyvisa-py pillow
* connect your instrument to the same subnet as your PC
* run ./scopemate.py -l. If the instrument is reachable its' ID will be returned, which looks like that: TCPIP::<ip address>::INSTR
* run ./scopemate.py -i TCPIP::<ip address>::INSTR . A screenshot of the specified instrument will be taken and saved into an image file named 'screenshot-<date,time>.png

Basic Usage

* Run ./scopemate.py -l. If the instrument is reachable its' ID will be returned
* Run ./scopemate.py -i TCPIP::<ip address>::INSTR . A screenshot of the specified instrument will be taken and saved into an image file named 'screenshot-<date,time>.png
* Run ./scopemate.py -i TCPIP::<ip address>::INSTR -m . A screenshot will be taken, default mask applied, and the result will be saved into an image file named 'screenshot-<date,time>.png

Other options:

'-s' - oscilloscope clock will be set to the current PC time.
'-c' - automatic measurement outputs at the bottom of the oscilloscope display will be turned off.
-C' - a comment will be added to the screenshot both on the screen and in the text chunk of PNG file. The comment text can either follow the '-C' flag on the command line or entered later interactively.

Masks:

Masks can be used to remove useless elements of the display to make it look less cluttered. If desired, right and left tabs, Rigol logo at top left, and trigger frequency output can be masked out. Provided masks can easily be customized in any image editor (I use Gimp), see Figures 3, and 5.  

