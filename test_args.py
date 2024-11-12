#!/usr/bin/env python3

# scopemate test suggested by llama3.2
import argparse
from subprocess import Popen, PIPE
import os

DEFAULT_MASK = ['mask-default-blank.png']

def test_scopemate(args):
    try:
        process = Popen(['python', 'scopemate.py'] + args, stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()
        if process.returncode != 0:
            print(f"Error: {error.decode('utf-8')}")
            return
        print(output.decode('utf-8'))
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Test scopemate.py functionality')
    parser.add_argument('-i', '--instrument', help='instrument to query')
    parser.add_argument('-l', '--list', help='list available instruments',
                        action='store_true')
    parser.add_argument('-m', '--mask', nargs='*', help='apply mask(s)')
    parser.add_argument('-o', '--output', help='output filename prefix')
    parser.add_argument('-s', '--synchronize', help='sync instrument\'s date and time with a PC',
                        action="store_true")
    parser.add_argument('-c', '--clean', help='turn off the measurements at the bottom of the screen',
                        action="store_true")

    args = parser.parse_args()

    if args.list:
        print("Available instruments:")
        test_scopemate(['-l'])
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
        
        test_scopemate(['-i', args.instrument, '-m', ','.join(args.mask), '-o', filename, '-s'])
        return

    print("Nothing to do. Use '-h' to get help")

if __name__ == "__main__":
    main()