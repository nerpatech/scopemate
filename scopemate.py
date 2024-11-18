#!/usr/bin/env python3
# Takes a screenshot of Rigol Oscilloscope. Compatible with DS2000 series, tested on MSO2302A
# In no particular order, inspired by:

import argparse
import time
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from PIL.PngImagePlugin import PngInfo
import pyvisa

DEFAULT_PREFIX = "screenshot"
DEFAULT_MASK = ["mask-default-blank.png"]
COMMENT_FONT = "NimbusMonoPS-Bold.otf"
COMMENT_FONT_SIZE = 20
COMMENT_POSITION = (50, 420)
COMMENT_COLOR = (255, 255, 255)
MAX_COMMENT_LENGTH = 60

CHUNK_SIZE = 1420  # set VISA chunk size equal to the Ethernet frame
# size. This improves transfer speed
TIMEOUT = 30000

rm = pyvisa.ResourceManager()


def query_oscilloscope(args: argparse.Namespace) -> None:
    img_text = None
    with rm.open_resource(args.instrument) as instr:
        instr.timeout = TIMEOUT
        instr.chunk_size = CHUNK_SIZE

        if args.clean:
            clean_screen(instr)

        if args.synchronize:
            sync_time(instr)

        if args.sysinfo or args.comment:
            img_text = add_text(instr, args)

        capture_screenshot(instr, args, img_text)

    instr.close()


def capture_screenshot(
    instr: pyvisa.Resource, args: argparse.Namespace, png_info: PngInfo
) -> None:
    instr.write(":DISPlay:DATA?")
    screenshot = instr.read_raw()[11:]  # discard BMP header
    im = Image.open(BytesIO(screenshot))
    im.putalpha(255)
    for mask in args.mask:
        overlay = Image.open(mask)
        im = Image.alpha_composite(im, overlay)

    if args.comment:
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(COMMENT_FONT, COMMENT_FONT_SIZE)
        draw.text(
            COMMENT_POSITION,
            args.comment,
            font=font,
            fill=COMMENT_COLOR,
        )

    if png_info:
        im.save(args.output, pnginfo=png_info)
    else:
        im.save(args.output)
    return


def add_text(
    instr: pyvisa.Resource, args: argparse.Namespace
) -> PngInfo:
    text_data = PngInfo()

    if args.sysinfo:
        sysinfo = (instr.query("*IDN?")).split(",")
        text_data.add_text("Manufacturer", sysinfo[0])
        text_data.add_text("Model", sysinfo[1])
        text_data.add_text("S/N", sysinfo[2])
        text_data.add_text("Firmware Version", sysinfo[3])
        calibration_date = instr.query("CALibrate:DATE?")
        calibration_time = instr.query("CALibrate:TIME?")
        text_data.add_text(
            "Calibration Date", calibration_date.replace(",", "-")
        )
        text_data.add_text(
            "Calibraton Time", calibration_time.replace(",", ":")
        )

    # Add comment to the text chunk if provided
    if args.comment:
        text_data.add_text("Comment", args.comment)

    return text_data


def clean_screen(instr: pyvisa.Resource) -> None:
    instr.query(":MEASure:CLEar ALL" + ";*OPC?")
    time.sleep(1)
    print("Measurements cleaned")


def sync_time(instr: pyvisa.Resource) -> None:
    date_time = datetime.now().strftime("%Y,%m,%d %H,%M,%S").split(" ")
    instr.query("SYSTem:DATE " + date_time[0] + ";*OPC?")
    instr.query("SYSTem:TIME " + date_time[1] + ";*OPC?")
    print("Oscilloscope clock set to PC time")


def main(args: argparse.Namespace) -> None:
    # if -l is specified all other parameters are silently ignored
    if args.list:
        print(rm.list_resources())
        return

    # specify default filename if '-o' is omitted
    if args.output:
        pass
    else:
        args.output = DEFAULT_PREFIX

    args.output = (
        args.output
        + "-"
        + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        + ".png"
    )

    # specify default mask if not provided with '-m'
    if args.mask:
        pass
    elif args.mask is None:  # New condition for no -m parameter
        args.mask = []  # Empty list means no masks
    else:
        args.mask = DEFAULT_MASK

    # Handle comment input if -C was specified but no comment provided
    if args.comment is not None and not args.comment.strip():
        try:
            args.comment = input(
                "Enter comment (max 255 chars) or press Enter to skip: "
            ).strip()

        except (KeyboardInterrupt, EOFError):
            print("\nComment input cancelled")
            args.comment = None

    if args.comment:
        args.comment = args.comment[:MAX_COMMENT_LENGTH]

    query_oscilloscope(args)
    return


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-l",
        "--list",
        help="list available instruments",
        action="store_true",
    )
    group.add_argument("-i", "--instrument", help="instrument to query")

    parser.add_argument("-m", "--mask", nargs="*", help="apply mask(s)")
    parser.add_argument("-o", "--output", help="output filename prefix")
    parser.add_argument(
        "-s",
        "--synchronize",
        help="set instrument's date and time to PC time",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--clean",
        help="turn off the automatic measurements output at the bottom of the display",
        action="store_true",
    )
    parser.add_argument(
        "-C",
        "--comment",
        help="add comment to screenshot as well as text data to PNG file (max "
        + str(MAX_COMMENT_LENGTH)
        + " chars). If empty, will prompt for input",
        nargs="?",
        const="",
    )
    parser.add_argument(
        "-S",
        "--sysinfo",
        help="add system information as text data to PNG file",
        action="store_true",
    )

    args = parser.parse_args()

    main(args)
