"""Adds a border to an image, with padding if needed.

To see usage options, run `python main.py --help`.

Saves a new version of the original image, with _bordered
  inserted into the filename:
  input_image.png -> input_image_bordered.png
"""

from cli import parse_cli_args
from image_processing import add_border

def main():
    """Parse CLI options, modify the image, and display a confirmation
    message.
    """
    # Get the filename and options from the CLI.
    path, options = parse_cli_args()

    # Add border to image and save the new image.
    new_img_path = add_border(path, options)
    print(f"New image saved at {new_img_path}")

if __name__ == "__main__":
    main()
