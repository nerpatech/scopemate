#!/usr/bin/env python3

import argparse
from pathlib import Path
from PIL import Image
import glob

def extract_png_info(filename: str, verbose: bool = False) -> None:
    """Extract and display PNG text chunks from image file.
    
    Args:
        filename: Path to PNG file
        verbose: If True, print all text chunks; if False, only print comment
    """
    try:
        with Image.open(filename) as img:
            # Check if image has text chunks
            if not hasattr(img, 'text'):
                if verbose:
                    print(f"{filename}: No text chunks found")
                return

            if verbose:
                # Print all text chunks
                print(f"\n{filename} text chunks:")
                for key, value in img.text.items():
                    print(f"{key}: {value}")
            else:
                # Print only comment if present
                if "User Comment" in img.text:
                    print(f"{filename}: {img.text['User Comment']}")
                
    except (OSError, SyntaxError) as e:
        print(f"Error processing {filename}: {str(e)}")
    except Exception as e:
        print(f"Unexpected error with {filename}: {str(e)}")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract comments from PNG files created by scopemate"
    )
    parser.add_argument(
        "files", 
        help="PNG file(s) to process. Accepts wildcards", 
        nargs="+")
    parser.add_argument(
        "-v", 
        "--verbose",
        action="store_true",
        help="Print all text chunks, not just comments")
    
    args = parser.parse_args()

    # Process all matching files
    for pattern in args.files:
        # Handle wildcards using glob
        matching_files = glob.glob(pattern)
        if not matching_files:
            print(f"No files found matching pattern: {pattern}")
            continue
            
        for filename in matching_files:
            if not filename.lower().endswith('.png'):
                print(f"Skipping non-PNG file: {filename}")
                continue
                
            extract_png_info(filename, args.verbose)

if __name__ == "__main__":
    main()
