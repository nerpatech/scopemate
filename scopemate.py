#!/usr/bin/env python3
# Takes a screenshot of Rigol Oscilloscope. Compatible with DS2000 series, tested on MSO2302A
# In no particular order, inspired by:
#   https://github.com/rdpoor/rigol-grab
#   https://github.com/RoGeorge/DS1054Z_screen_capture
#   https://github.com/ronangaillard/rigol-screen-capture
#   https://github.com/bveina/Rigol-Scope-Snap
#   https://github.com/gnbl/DS1000Z
#   https://github.com/MichaelSasser/ds2000
#   https://github.com/pklaus/ds1054z

import argparse
import time
from datetime import datetime
from io import BytesIO
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import pyvisa

CHUNK_SIZE = 1420   # set VISA chunk size equal to the Ethernet frame
                    # size. This improves transfer speed
TIMEOUT = 30000
DEFAULT_MASK = ['mask-default-blank.png']
do_clean = False
do_sync = False

parser = argparse.ArgumentParser()
rm = pyvisa.ResourceManager()

def get_screen(resource: pyvisa.Resource, filename: str,
               masks: list[str]) -> None:
    with rm.open_resource(resource) as instr:
        instr.timeout = TIMEOUT
        instr.chunk_size = CHUNK_SIZE
        name = filename + '-' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.png'
        if do_clean:
            clean_screen(instr)
        if do_sync:
            sync_time(instr)
        instr.write(':DISPlay:DATA?')
        screenshot = instr.read_raw()[11:] # discard BMP header
        im = Image.open(BytesIO(screenshot))
        im.putalpha(255)
        for mask in masks:
            overlay = Image.open(mask)
            im = Image.alpha_composite(im, overlay)
        im.save(name, pnginfo=add_data(instr))
    instr.close()

# add instrument information to the screenshot file
def add_data(instr) -> PngInfo:
    txt_data = PngInfo()
    sysinfo = (instr.query('*IDN?'))
    calibration_date = (instr.query('CALibrate:DATE?'))
    calibration_time = (instr.query('CALibrate:TIME?'))
    txt_data.add_text("System Information", sysinfo)
    txt_data.add_text("Calibration Date(Year, Month, Date)", calibration_date)
    txt_data.add_text("Calibraton Time", calibration_time)
    return txt_data

def clean_screen(instr: pyvisa.Resource) -> None:
    instr.query(':MEASure:CLEar ALL' + ';*OPC?')
    time.sleep(1)
    print("Measurements cleaned")

def sync_time(instr: pyvisa.Resource) -> None:
    date_time = (datetime.now().strftime('%Y,%m,%d %H,%M,%S').split(' '))
    instr.query('SYSTem:DATE ' + date_time[0] + ';*OPC?')
    instr.query('SYSTem:TIME ' + date_time[1] + ';*OPC?')
    print("Oscilloscope clock set to PC time")

def main() -> None:
    parser.add_argument("-i", "--instrument", help="instrument to query")
    parser.add_argument("-l", "--list", help="list available instruments",
                    action='store_true')
    parser.add_argument("-m", "--mask", nargs='*', help="apply mask(s)")
    parser.add_argument("-o", "--output", help="output filename prefix")
    parser.add_argument("-s", "--synchronize", help="sync instrument's \
                    date and time with a PC", action="store_true")
    parser.add_argument("-c", "--clean", help="turn off the \
                    measurements at the bottom of the screen",
                    action="store_true")

    args = parser.parse_args()    
    
    # if -l is specified all other parameters are silently ignored
    if args.list:
        print(rm.list_resources())
        return

    # Check for dependent arguments without -i being specified
    if not args.instrument and (args.mask is not None or args.clean or args.synchronize):
        print("Error: Options -m, -c, and -s require -i/--instrument to be specified")
        return

    if args.instrument:
        if args.output:
            filename = args.output
        else:
            filename = 'screenshot'

        if args.mask:
            pass
        elif args.mask is None:  # New condition for no -m parameter
            args.mask = []       # Empty list means no masks
        else: 
            args.mask = DEFAULT_MASK

        if args.clean:
            global do_clean
            do_clean = True

        if args.synchronize:
            global do_sync
            do_sync = True    
        
        get_screen(args.instrument, filename, args.mask)
        return

    print("Nothing to do. Use '-h' to get help")
if __name__ == "__main__":
    main()
