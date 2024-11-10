The purpose of this script is to automate the process of removing unnecessary information from oscilloscope screenshots making them easier to read. It captures the screenshot, applies one or more transparency masks and outputs the result into an image file.

The script takes several inputs:

A resource identifier (instrument address) that specifies the connection details to the oscilloscope.

An optional list of masks, which are images used to overlay on top of the screenshot filling the area(s) with black pixels.

An optional output filename prefix, which allows the user to specify a custom name for the saved screenshot.

The script produces two main outputs:

A PNG image file containing the modified screenshot.

If the synchronize option is enabled, it also updates the oscilloscope's date and time settings to match those of the computer running the script.

Included transparency masks are made for Rigol MSO2000 series oscilloscope screen layout.  The script should be with DS2000 series instruments. The functionality is tested on Rigol MSO2032A.

Installation

* install and activate a virtual environment 
* install dependencies: pip install pyvisa pyvisa-py pillow
* connect your instrument to the same subnet
* run python scopemate.py -l. If the instrument is reachable its' ID will be returned, which looks like that: TCPIP::<ip address>::INSTR
