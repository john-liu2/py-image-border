"""Initial tests of basic functionality."""

import subprocess, filecmp
from pathlib import Path

# --- Tests for correct usage. ---

def test_default_border():
    """Test that calling with just a filename works."""

    # Note: currently, modified image ends up in same dir as source image.
    path_source = Path("tests/source_images/bear_scratching.jpg")
    path_modified = Path("tests/source_images/bear_scratching_bordered.jpg")
    path_reference = Path("tests/reference_images/bear_scratching_default.jpg")

    cmd = f"python -m py_image_border.add_border {path_source}"
    cmd_parts = cmd.split()

    output = subprocess.run(cmd_parts, capture_output=True)
    output_str = output.stdout.decode()
    assert filecmp.cmp(path_modified, path_reference)
    assert f"New image saved at {path_modified}" in output_str

def test_15px_border():
    """Test that calling with a filename and custom border width works."""

    # Note: currently, modified image ends up in same dir as source image.
    path_source = Path("tests/source_images/bear_scratching.jpg")
    path_modified = Path("tests/source_images/bear_scratching_bordered.jpg")
    path_reference = Path("tests/reference_images/bear_scratching_15px_border.jpg")

    cmd = f"python -m py_image_border.add_border {path_source} 15"
    cmd_parts = cmd.split()

    subprocess.run(cmd_parts)
    assert filecmp.cmp(path_modified, path_reference)

def test_padding_only():
    """Test that you can add padding to an image."""
    # Note: currently, modified image ends up in same dir as source image.
    path_source = Path("tests/source_images/bear_scratching.jpg")
    path_modified = Path("tests/source_images/bear_scratching_bordered.jpg")
    path_reference = Path("tests/reference_images/bear_scratching_15px_padding.jpg")

    cmd = f"python -m py_image_border.add_border {path_source} --padding 15"
    cmd_parts = cmd.split()

    subprocess.run(cmd_parts)
    assert filecmp.cmp(path_modified, path_reference)

def test_custom_color_only():
    """Test that you can set a custom border color."""
    # Note: currently, modified image ends up in same dir as source image.
    path_source = Path("tests/source_images/bear_scratching.jpg")
    path_modified = Path("tests/source_images/bear_scratching_bordered.jpg")
    path_reference = Path("tests/reference_images/bear_scratching_black_border.jpg")

    cmd = f"python -m py_image_border.add_border {path_source} --border-color black"
    cmd_parts = cmd.split()

    subprocess.run(cmd_parts)
    assert filecmp.cmp(path_modified, path_reference)

def test_padding_and_border():
    """Test that you can set custom padding and border width."""
    # Note: This is just one test for combinining options; would add more of
    #   these tests in a widely-used version of the project.

    # Note: currently, modified image ends up in same dir as source image.
    path_source = Path("tests/source_images/bear_scratching.jpg")
    path_modified = Path("tests/source_images/bear_scratching_bordered.jpg")
    path_reference = Path("tests/reference_images/bear_scratching_20px_border_15px_padding.jpg")

    cmd = f"python -m py_image_border.add_border {path_source} 20 --padding 15"
    cmd_parts = cmd.split()

    subprocess.run(cmd_parts)
    assert filecmp.cmp(path_modified, path_reference)

def test_make_transparent():
    """Test that making the background transparent works."""
    # Note: currently, modified image ends up in same dir as source image.
    path_source = Path("tests/source_images/gh_screenshot.png")
    path_modified = Path("tests/source_images/gh_screenshot_bordered.png")
    path_reference = Path("tests/reference_images/gh_screenshot_transparent.png")

    cmd = f"python -m py_image_border.add_border {path_source} 0 --make-transparent"
    cmd_parts = cmd.split()

    subprocess.run(cmd_parts)
    # assert filecmp.cmp(path_modified, path_reference)
    # JL 2025-08-12: Fix: the metadata or compression can make PNG files binary
    # different even if they look the same. We should use Pillow library to do pixel
    # equality comparison.
    from PIL import Image, ImageChops

    def images_are_equal(img1_path, img2_path):
        img1 = Image.open(img1_path).convert("RGB")
        img2 = Image.open(img2_path).convert("RGB")
        return ImageChops.difference(img1, img2).getbbox() is None

    assert images_are_equal(path_modified, path_reference)


# --- Tests for incorrect usage. ---

def test_no_arg():
    """Test that calling without a filename specified generates correct error msg."""
    cmd = f"python -m py_image_border.add_border"
    cmd_parts = cmd.split()

    output = subprocess.run(cmd_parts, capture_output=True)
    error_msg = output.stderr.decode()

    assert "error: the following arguments are required: path" in error_msg

    # error_msg = output.stdout.decode()
    # assert "You must provide a target image." in error_msg

def test_nonexistent_file():
    """Test that calling with a nonexistent file generates a correct error msg."""
    path_source = Path("tests/source_images/nonexistent_file.txt")

    cmd = f"python -m py_image_border.add_border {path_source}"
    cmd_parts = cmd.split()

    output = subprocess.run(cmd_parts, capture_output=True)
    error_msg = output.stdout.decode()

    assert "nonexistent_file.txt does not seem to exist." in error_msg

def test_invalid_image_file():
    """Test that calling with an invalid image file generates correct error msg."""
    path_source = Path("tests/source_images/hello.txt")

    cmd = f"python -m py_image_border.add_border {path_source}"
    cmd_parts = cmd.split()

    output = subprocess.run(cmd_parts, capture_output=True)
    error_msg = output.stdout.decode()

    assert "hello.txt does not seem to be an image file." in error_msg
