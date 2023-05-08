"""CLI for the add_border project.

Defines an Options dataclass, containing options specified
  over the command line.

Also defines a function that parses the CLI arguments.

Validates that the target file exists.
"""

import sys
import argparse
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Options:
    border_width: int
    padding: int
    border_color: str
    make_transparent: bool

def parse_cli_args():
    """Parse all options from the CLI.
    The path is treated separately, as it is distinct from border
      options.

    Returns:
    Tuple containing:
        Path: Path to the original image file.
        Options: An instance of the Options dataclass.
    """

    parser = argparse.ArgumentParser(
            description="Add a border to any image.")

    # Parse the path to the original image.
    parser.add_argument("path", type=Path,
            help="Path to the original image.")

    # Parse options for the border.
    parser.add_argument("border_width", type=int,
            nargs="?",default=2,
            help="Border width (default: 2).")
    parser.add_argument("--padding", type=int, default=0,
            help="Padding (default: 0).")
    parser.add_argument("--border-color",
            dest="border_color", default="lightgray",
            help="Border color (default: lightgray).")
    parser.add_argument("--make-transparent",
            dest="make_transparent", action="store_true",
            help="Make the background transparent (default: False).")

    # Define options.
    args = parser.parse_args()

    # Make sure the requested file exists.
    path = args.path
    if not path.exists():
        print(f"{path} does not seem to exist.")
        sys.exit()

    options = Options(args.border_width, args.padding,
            args.border_color, args.make_transparent)

    return path, options
