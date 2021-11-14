import argparse
import logging
import os
from PIL import Image
import re

import scriptbase.utils.file_handling.file_utils as file_utils
import scriptbase.utils.file_handling.image_utils as image_utils
import scriptbase.utils.magic_the_gathering.cockatrice as cockatrice

this_logger = logging.getLogger(__loader__.name)

## Various global coordinates that can be configured if necessary
ARTIST_X_RANGE = range(140, 320)
ARTIST_Y_RANGE = range(990, 1013)

ARTIST_X_RANGE_POST_MPC_READY = range(103, 342)
ARTIST_Y_RANGE_POST_MPC_READY = range(1018, 1040)

ARTIST_X_RANGE_PLANESWALKER_POST_MPC_READY = range(80, 130)
ARTIST_Y_RANGE_PLANESWALKER_POST_MPC_READY = range(1005, 1030)

COPYRIGHT_X_RANGE = range(440, 698)
COPYRIGHT_Y_RANGE_CREATURE = range(986, 1000)
COPYRIGHT_Y_RANGE_NONCREATURE = range(969, 984)

CORNER_RANGES = [(range(0, 35), range(0, 34)),
                 (range(710, 744), range(0, 34)),
                 (range(0, 35), range(1006, 1039)),
                 (range(708, 744), range(1006, 1039))]

NOT_FOR_SALE_X_RANGE = range(168, 276)
NOT_FOR_SALE_Y_RANGE = range(972, 988)

MPC_ADJUSTED_DIMENSIONS = (816, 1110)


def parse_args():

    parser = argparse.ArgumentParser(description="Turns standard card images to MPC ready card images - designed "
                                                 "for https://mtg.design but not necessary for it")

    parser.add_argument("-o", "--output", help="Location where files should be output", required=True)
    parser.add_argument("-i", "--input", help="Location of folder containing card images", required=True)
    parser.add_argument("-v", "--valid-extensions", default=["jpg", "png"], help="List of valid image extensions",
                        nargs='+')
    parser.add_argument("-c", "--cockatrice-xml", help="More accurately erase copyright by passing a cockatrice XML "
                                                       "of the set")
    parser.add_argument("-r", "--regex-name-match", help="Fancy name matching to extract a card name from a file name, "
                                                         "e.g. [\d]+_(.+)",
                        default="(.+)")
    parser.add_argument("--corner-scrub-color", nargs="+", type=int,
                        help="Color to scrub the corners with as RGB(A), only used if -R is set", default=[0, 0, 0])
    ## [\d]+_(.+) - what the dndmtg set uses, second capture group

    ## Flags
    parser.add_argument("-A", "--scrub-artist", help="Erases the artist from the card image", action="store_true")
    parser.add_argument("-R", "--scrub-corners", help="Erases the corners - useful if the corners are white",
                        action="store_true")
    parser.add_argument("-N", "--scrub-not-for-sale", help="Erases the 'Not For Sale' text present on "
                                                           "https://mtg.design cards",
                        action="store_true")
    parser.add_argument("-C", "--scrub-copyright", help="Erases the WOTC copyright information from the card",
                        action="store_true")
    parser.add_argument("--raise-errors", help="Raises the errors in full rather than silencing them and proceeding.",
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

    cockatrice_database = None
    if args.cockatrice_xml:
        this_logger.warning(f"LOADING COCKATRICE DATABASE...")
        cockatrice_database = cockatrice.CockatriceDatabase()
        cockatrice_database.parse_xml(path=args.cockatrice_xml)

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

    i = 0
    for image_path in valid_files:

        i += 1
        this_logger.warning(f"({i}/{total}) Processing file {image_path}...")

        try:
            im_filename = os.path.splitext(os.path.basename(image_path))[0]
            card_name_match = re.match(args.regex_name_match, im_filename)
            if not card_name_match:
                this_logger.error(f"--- Skipping {im_filename} because it fails the card name regex match check. ---")
                continue
            card_name = card_name_match.group(1)

            im: Image.Image = Image.open(image_path)

            card_is_creature = True
            if cockatrice_database is not None:
                card = cockatrice_database.card_data.get(card_name)
                if card is not None:
                    card_is_creature = card.type.lower() == "creature" or card.type.lower() == "planeswalker"

            if args.scrub_artist:
                image_utils.scrub(im, ((x, y) for x in ARTIST_X_RANGE_POST_MPC_READY for y in ARTIST_Y_RANGE_POST_MPC_READY))

            if args.scrub_copyright:
                if card_is_creature:
                    this_logger.info(f"--- Inputted file is a creature or planeswalker, "
                                     f"using a different range for removing "
                                     f"copyright ---")
                    image_utils.scrub(im, ((x, y) for x in COPYRIGHT_X_RANGE for y in COPYRIGHT_Y_RANGE_CREATURE))
                else:
                    this_logger.info(f"--- Inputted file is non-creature, using standard range for removing "
                                     f"copyright ---")
                    image_utils.scrub(im, ((x, y) for x in COPYRIGHT_X_RANGE for y in COPYRIGHT_Y_RANGE_NONCREATURE))

            if args.scrub_corners:
                for x_range, y_range in CORNER_RANGES:
                    image_utils.scrub(im,
                                      ((x, y) for x in x_range for y in y_range),
                                      scrub_color=tuple(args.corner_scrub_color))

            if args.scrub_not_for_sale:
                image_utils.scrub(im, ((x, y) for x in NOT_FOR_SALE_X_RANGE for y in NOT_FOR_SALE_Y_RANGE))

            #im = image_utils.resize_canvas(im, *MPC_ADJUSTED_DIMENSIONS, new_background=(0, 0, 0) if len(im.mode) == 3 else (0, 0, 0, 255))
            im.save(os.path.join(args.output, os.path.basename(im_filename)) + ".png")
            im.close()

        except Exception as e:
            if args.raise_errors:
                raise e
            this_logger.error(f"An error occurred! {e}")

if __name__ == "__main__":
    main()

