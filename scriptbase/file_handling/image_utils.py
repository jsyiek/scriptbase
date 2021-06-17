from PIL import Image
from typing import List, Tuple, Optional

def scrub(image: Image.Image, coords, scrub_color: tuple = (0, 0, 0)) -> Image.Image:
    """
    Sets the all pixels in the coord range to black, i.e. (0, 0, 0)

    Parameters:
          image (Image.Image): Image object to use
          coords (Iterable): List of integer tuples of coords
          scrub_color (tuple): Color to scrub the pixels with

    Returns:
          image (Image.Image): Inputted image, scrubbed
    """

    for c in coords:
        image.putpixel(c, scrub_color)

    return image


def resize_canvas(image: Image.Image, new_x: int, new_y: int, new_background: tuple = None) -> Image.Image:
    """
    Resizes the canvas of the image, centering the image on the new canvas.

    Parameters:
         image (Image.Image): Image object to resize canvas on
         new_x (int): X size of new canvas
         new_y (int): Y size of new canvas
         new_background (tuple): Tuple of the new color to use

    Returns:
        canvas_resized_image (Image.Image): Canvas resized version of input image
    """

    x_offset = (new_x - image.size[0]) // 2
    y_offset = (new_y - image.size[1]) // 2

    mode = image.mode
    if new_background is None:
        if len(mode) == 1:
            new_background = (255,)
        if len(mode) == 3:
            new_background = (255, 255, 255)
        if len(mode) == 4:
            new_background = (255, 255, 255, 255)
    elif len(new_background) != len(mode):
        raise ValueError(f"Input background color is of length {len(new_background)}, but image mode is {len(mode)}!")

    return_image = Image.new(mode, (new_x, new_y), new_background)
    return_image.paste(image, (x_offset, y_offset, x_offset + image.size[0], y_offset + image.size[1]))

    return return_image
