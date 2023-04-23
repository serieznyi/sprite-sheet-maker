import argparse
import logging
import math
import os
import time

from pathlib import Path
from PIL import Image

DEFAULT_COLUMNS_COUNT = 5

# Logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)


def read_images(source_dir: Path) -> list:
    files = sorted(source_dir.glob('**/*'))
    frames = []

    for current_file in files:
        logger.debug("Read file: %s" % current_file)
        try:
            with Image.open(current_file) as im:
                frames.append(im.getdata())
        except Exception as e:
            raise RuntimeError("'%s' is not a valid image" % current_file, e)

    return frames


def generate_sprite_sheet(source_dir: Path, output_dir: Path, rows: int | None, columns: int | None) -> None:
    logger.info("Source dir: %s" % source_dir)
    logger.info("Output dir: %s" % output_dir)

    frames = read_images(source_dir)
    frames_count = len(frames)

    if frames_count == 0:
        logger.warning("Source dir is empty")
        return

    logger.info("Source images count: %s" % frames_count)

    max_columns = columns if columns else DEFAULT_COLUMNS_COUNT
    max_rows = rows if rows else math.ceil(len(frames) / DEFAULT_COLUMNS_COUNT)

    logger.info("Grid size: columns = %s, rows = %s" % (max_columns, max_rows))

    tile_width = frames[0].size[0]
    tile_height = frames[0].size[1]

    sprite_sheet_width = int(tile_width * max_columns)
    sprite_sheet_height = tile_height * max_rows

    print(sprite_sheet_width, sprite_sheet_height)

    sprite_sheet = Image.new("RGBA", (sprite_sheet_width, sprite_sheet_height))

    # ((0, 0), (500, 500))
    # ((0, 500), (1000, 500))
    # ((0, 1000), (1500, 500))
    # ((0, 1500), (2000, 500))
    # ((0, 2000), (2500, 500))

    for frame in frames:
        cropped_frame = frame.crop((0, 0, tile_width, tile_height))
        frame_index = frames.index(frame)

        if frame_index > max_rows * max_columns:
            print("ASD")
            break

        # (x1,y1)------------|
        #    |               |
        #    |               |
        #    |------------(x2,y2)
        x1 = tile_height * (frame_index % max_columns)
        y1 = tile_width * math.floor(frame_index / max_columns)

        x2 = x1 + tile_width
        y2 = y1 + tile_height

        box = (x1, y1, x2, y2)

        print(frame_index,
              math.floor(frame_index / max_columns),
              (frame_index % max_columns),
              box
              )

        sprite_sheet.paste(cropped_frame, box)

    sprite_sheet_file_name = "sprite_sheet" + time.strftime("%Y%m%dT%H%M%S") + ".png"
    sprite_sheet.save(Path(output_dir, sprite_sheet_file_name), "PNG")


def main():
    options = parse_args()

    logger.setLevel(eval('logging.' + options.logLevel.upper()))

    generate_sprite_sheet(
        source_dir=options.sourceDir,
        output_dir=options.outputDir,
        rows=options.rows,
        columns=options.columns
    )


def argparse_validation_dir_path(mode: int):
    """

    :type mode: os.R_OK or os.W_OK
    """

    def validator(value):
        directory = Path(value)

        if not directory.is_dir():
            raise argparse.ArgumentTypeError("Not a directory: %s" % value)

        if mode == os.R_OK and not os.access(directory, os.R_OK):
            raise argparse.ArgumentTypeError("File %s not readable" % value)
        elif mode == os.W_OK and not os.access(directory, os.W_OK):
            raise argparse.ArgumentTypeError("File %s not writable" % value)

        return directory.absolute()

    return validator


def argparse_validation_int(minimal_value: int = 1):
    def validation(value):
        try:
            value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError("Must be a integer number")
        if value < minimal_value:
            raise argparse.ArgumentTypeError("Argument must be > " + str(minimal_value))
        return value

    return validation


def parse_args():
    parser = argparse.ArgumentParser(
        description='''
                Generate spritesheet image
            ''',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        'sourceDir',
        type=argparse_validation_dir_path(os.R_OK),
        help="Directory with source images for spritesheet generating"
    )

    parser.add_argument(
        'outputDir',
        type=argparse_validation_dir_path(os.W_OK),
        help="Directory for result"
    )

    parser.add_argument(
        '--rows',
        type=argparse_validation_int(1),
        help="Columns count"
    )

    parser.add_argument(
        '--columns',
        type=argparse_validation_int(1),
        help="Rows count"
    )

    parser.add_argument(
        '--logLevel',
        default='info',
        help="Logging level. Default: info",
        choices=['info', 'debug', 'warn']
    )

    return parser.parse_args()


if __name__ == '__main__':
    main()
