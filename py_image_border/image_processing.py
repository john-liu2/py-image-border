"""This module handles all work associated with adding a border to an image."""

from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError
from .cli import Options


def make_background_transparent(img, threshold=10):
    img = img.convert("RGBA")
    bg_color = img.getpixel((0, 0))
    transparent_color = (0, 0, 0, 0)

    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            if all(abs(pixel[i] - bg_color[i]) <= threshold for i in range(3)):
                img.putpixel((x, y), transparent_color)

    return img


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

    # We want to work on a copy of the original image.
    new_img = img.copy()

    # Deal with transparency before adding any borders or padding,
    #   because transparency assumes the top left pixel
    #   is the background color.
    # This doesn't work particularly well. Consider exposing threshold
    #   as a CLI arg. Also consider looking at more complex ways of 
    #   adding transparency. For example in the sample image I used, the
    #   logo elements were shaded. This would probably work better on
    #   an image where all colored elements had no shading, ie their
    #   pixels were all one color.
    # Would also reconsider exactly how the threshold is used for each pixel.
    if options.make_transparent:
        new_img = make_background_transparent(new_img, threshold=40)

    new_img = ImageOps.expand(new_img, border=options.padding, fill="white")
    new_img = ImageOps.expand(new_img, border=options.border_width,
            fill=options.border_color)

    new_path = (path.parent / f"{path.stem}_bordered{path.suffix}")
    new_img.save(new_path)

    return new_path
