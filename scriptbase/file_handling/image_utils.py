from PIL import Image
from typing import List, Tuple

def scrub(image: Image.Image, coords) -> Image.Image:
    """
    Sets the all pixels in the coord range to black, i.e. (0, 0, 0)

    Parameters:
          image (Image.Image): Image object to use
          coords (Iterable): List of integer tuples of coords

    Returns:
          image (Image.Image): Inputted image, scrubbed
    """

    for c in coords:
        image.putpixel(c, (0, 0, 0))

    return image
