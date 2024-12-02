#!/usr/bin/env python3

import argparse
import glob
from pathlib import Path
from PIL import Image


def extract_png_info(filename: str) -> None:
    """Extract and display PNG text chunk from image file.

    Args:
        filename: Path to PNG file

    """
    try:
        with Image.open(filename) as img:
            # Check if image has text chunks
            if not img.text:
                return

            print(f"\n{filename}:")
            for key, value in img.text.items():
                print(f"{key}: {value}")

    except (OSError, SyntaxError) as e:
        print(f"Error processing {filename}: {str(e)}")
    except Exception as e:
        print(f"Unexpected error with {filename}: {str(e)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract text from PNG files created by scopemate"
    )
    parser.add_argument(
        "files",
        help="PNG file(s) to process. Accepts wildcards",
        nargs="+",
    )

    args = parser.parse_args()

    # Process all matching files
    for pattern in args.files:
        # Handle wildcards using glob
        matching_files = glob.glob(pattern)
        if not matching_files:
            print(f"No files found matching pattern: {pattern}")
            continue

        for filename in matching_files:
            if not filename.lower().endswith(".png"):
                print(f"Skipping non-PNG file: {filename}")
                continue

            extract_png_info(filename)


if __name__ == "__main__":
    main()
