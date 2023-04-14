"""This module handles all work associated with adding a border to an image."""

from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError
from cli import Options

def add_border(path: Path, options: Options):
    """Add a border to an image.
    Also adds padding if requested, and saves the modified image.

    The new filename is the original filename, with _bordered inserted:
    - input_image.png -> input_image_bordered.png

    Returns:
    Path: Path where the modified image was saved.
    """
    try:
        img = Image.open(path)
    except UnidentifiedImageError:
        print(f"{path} does not seem to be an image file.")
        sys.exit()

    new_img = ImageOps.expand(img, border=options.padding, fill="white")
    new_img = ImageOps.expand(new_img, border=options.border_width,
            fill=options.border_color)

    new_path = (path.parent / f"{path.stem}_bordered{path.suffix}")
    new_img.save(new_path)

    return new_path
