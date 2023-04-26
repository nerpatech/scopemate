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
from datetime import datetime
from io import BytesIO
from PIL import Image
import pyvisa

parser = argparse.ArgumentParser()
rm = pyvisa.ResourceManager()

def get_screen(resource, filename, masks):

    instr = rm.open_resource(resource)
    instr.timeout = 30000
    instr.chunk_size = 1420     # magic number for faster speed

    name = filename + '-' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.png'
    instr.write(':DISPlay:DATA?')
    screenshot = instr.read_raw()[11:] # discard BMP header
    im = Image.open(BytesIO(screenshot))
    im.putalpha(255)
    for mask in masks:
        overlay = Image.open(mask)
        im = Image.alpha_composite(im, overlay)
    im.save(name)
    instr.close()

def set_time(resource):

    instr = rm.open_resource(resource)
    instr.timeout = 30000
    instr.chunk_size = 1420     # magic number for faster speed

    date_time = (datetime.now().strftime('%Y,%m,%d %H,%M,%S').split(' '))
    instr.query('SYSTem:DATE ' + date_time[0] + ';*OPC?')
    instr.query('SYSTem:TIME ' + date_time[1] + ';*OPC?')
    instr.close()




parser.add_argument("-i", "--instrument", help="instrument to query")
parser.add_argument("-l", "--list", help="list available instruments",
                    action='store_true')
parser.add_argument("-m", "--mask", help="apply mask(s)", nargs='+', default=[])
parser.add_argument("-o", "--output", help="output filename prefix")
parser.add_argument("-s", "--synchronize", help="sync instrument's \
                    date and time with a PC", action="store_true")

args = parser.parse_args()

if args.list:
    print(rm.list_resources())
    exit()


if args.instrument:
    if args.output:
        filename = args.output
    else:
        filename = 'screenshot'

if args.synchronize:
    if args.instrument:
        set_time(args.instrument)
    else:
        print("-i required")
    exit()

get_screen(args.instrument, filename, args.mask)
exit()

print("Nothing to do. Use '-h' to get help")
