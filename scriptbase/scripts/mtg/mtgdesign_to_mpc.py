import argparse
import logging
import os
from PIL import Image
import tempfile

import scriptbase.file_handling.file_utils as file_utils
import scriptbase.file_handling.image_utils as image_utils


this_logger = logging.getLogger(__loader__.name)

## Various global coordinates that can be configured if necessary
ARTIST_X_RANGE = range(140, 320)
ARTIST_Y_RANGE = range(990, 1013)

COPYRIGHT_X_RANGE_CREATURE = range(440, 698)
COPYRIGHT_Y_RANGE_CREATURE = range(986, 1000)


def parse_args():

    parser = argparse.ArgumentParser(description="Turns standard card images to MPC ready card images - designed "
                                                 "for https://mtg.design but not necessary for it")

    parser.add_argument("-o", "--output", help="Location where files should be output", required=True)
    parser.add_argument("-i", "--input", help="Location of folder containing card images", required=True)
    parser.add_argument("-v", "--valid-extensions", default=["jpg", "png"], help="List of valid image extensions",
                        nargs='+')

    ## Flags
    parser.add_argument("-A", "--scrub-artist", help="Erases the artist from the card image", action="store_true")
    parser.add_argument("-R", "--scrub-corners", help="Erases the corners - useful if the corners are white",
                        action="store_true")
    parser.add_argument("-N", "--scrub-not-for-sale", help="Erases the 'Not For Sale' text present on "
                                                           "https://mtg.design cards",
                        action="store_true")
    parser.add_argument("-C", "--scrub-copyright", help="Erases the WOTC copyright information from the card",
                        action="store_true")

    return parser.parse_args()


def main():
    args = parse_args()

    ## Verify input path exists
    if not os.path.exists(args.input):
        this_logger.critical(f"The input path does not exist! {args.input}")
        exit(1)
    elif not os.path.isdir(args.input):
        this_logger.critical(f"The input path is not a folder! {args.input}")
        exit(1)

    ## Verify output arg
    if os.path.exists(args.output) and not os.path.isdir(args.output):
        this_logger.critical(f"The output path exists and is not a directory! {args.output}")
        exit(1)
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    valid_files = file_utils.recursive_file_grab(args.valid_extensions, args.input)
    valid_files.sort()

    ## Log the files we find
    this_logger.warning(f"============================================")
    this_logger.warning(f"                 FOUND FILES                ")
    i = 1
    total = len(valid_files)
    for image_path in valid_files:
        this_logger.warning(f"({i}/{total}) {image_path}")
        i += 1
    this_logger.warning(f"============================================")

    i = 1
    for image_path in valid_files:
        this_logger.warning(f"({i}/{total}) Processing file {image_path}...")

        try:
            im: Image.Image = Image.open(image_path)

            if args.scrub_artist:
                image_utils.scrub(im, ((x, y) for x in ARTIST_X_RANGE for y in ARTIST_Y_RANGE))

            if args.scrub_copyright:
                image_utils.scrub(im, ((x, y) for x in COPYRIGHT_X_RANGE for y in COPYRIGHT_Y_RANGE))

            im.save(os.path.join(args.output, os.path.basename(image_path)))

        except Exception as e:
            this_logger.error(f"An error occurred! {e}")

        exit()

if __name__ == "__main__":
    main()

