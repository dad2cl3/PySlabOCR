import json, os, pytesseract, re

from glob import glob
# from os import listdir
from PIL import Image
from shutil import copyfile
from sys import path


def read_source_dir(source_dir):
    short_files = []
    long_files = glob(source_dir)
    long_files.sort()

    for long_file in long_files:
        short_files.append(os.path.basename(long_file))

    return short_files


def build_image_pairs(images):
    # script assumes front is scanned and then back is scanned for same card
    # script assumes both scans are performed in order before another card is scanned
    # script assumes timestamp order will ensure front and back of same card are consecutive files in directory listing
    image_count = len(images)
    pairs = []
    for i in range(0, image_count, 2):
        pair = [images[i], images[i+1]]
        pairs.append(pair)

    return pairs


def read_image_char(target_img):
    text = pytesseract.image_to_string(Image.open('{0}{1}'.format(slab_config['paths']['raw'], target_img)))

    return text


def find_cert(image_text):

    search_pattern = re.compile('[0-9]{8}', re.MULTILINE)
    search_results = search_pattern.search(image_text)

    if search_results is not None:
        cert = search_results[0]
    else:
        cert = slab_config['default_cert']

    return cert


def write_target_dir(images):
    # assumes there could be one or more images in the images object
    # print(images)

    source_dir = images['directories']['source']
    target_dir = images['directories']['target']

    for image in images['images']:
        source_file = '{0}{1}'.format(source_dir, image['source']['name'])
        target_file = '{0}{1}'.format(target_dir, image['target']['name'])
        # print(source_file, target_file)
        copyfile(source_file, target_file)

    # return 'something'


def build_composite_image(images):
    left_image = Image.open('{0}{1}'.format(slab_config['paths']['raw'], images[0]))
    right_image = Image.open('{0}{1}'.format(slab_config['paths']['raw'], images[1]))

    left_width, left_height = left_image.size
    right_width, right_height = right_image.size

    background_width = left_width + right_width # assumes vertical slabs only
    background_height = left_height

    # create the composite image
    composite = Image.new(mode='RGBA', size=(background_width, background_height))
    # copy left image to composite
    composite.paste(im=left_image, box=(0, 0))
    # copy right image to composite
    composite.paste(im=right_image, box=(left_width, 0))

    return composite


def build_square_image(images):
    left_image = Image.open('{0}{1}'.format(slab_config['paths']['raw'], images[0]))
    right_image = Image.open('{0}{1}'.format(slab_config['paths']['raw'], images[1]))

    left_width, left_height = left_image.size
    right_width, right_height = right_image.size

    if left_width + right_width > left_height:
        background_width = background_height = left_width + right_width # assumes vertical slabs only
        # centers the two images vertically in the black space
        top_x = [0, left_width]
        top_y = int((background_height - left_height) / 2)
    else:
        background_width = background_height = right_height
        top_x = [int((background_width - left_width / 2)), int((background_width - left_width) / 2 + right_width)]
        top_y = 0

    # create the composite image
    square = Image.new(mode='RGBA', size=(background_width, background_height))
    # copy left image to composite
    square.paste(im=left_image, box=(top_x[0], top_y))
    # copy right image to composite
    square.paste(im=right_image, box=(top_x[1], top_y))

    return square


if __name__ == '__main__':
    # load the config
    with open('config.json', 'r') as config_file:
        slab_config = json.load(config_file)

    # add raw and final paths to script path
    path.append(slab_config['paths']['raw'])
    path.append(slab_config['paths']['final'])

    # read the source directory
    raw_count = 0
    manual_count = 0
    raw_files = read_source_dir('{0}*{1}'.format(slab_config['paths']['raw'], slab_config['image_ext']))

    # must have even number of files
    if len(raw_files) % 2 == 0:
        image_pairs = build_image_pairs(raw_files)
        raw_count = len(image_pairs)
        # print(image_pairs)
        processed = 0
        for image_pair in image_pairs:
            front_image = image_pair[0]
            image_text = read_image_char(front_image)
            # print(image_text) # debug
            cert = find_cert(image_text)

            if cert == slab_config['default_cert']:
                # open the image file
                Image.open('{0}{1}'.format(slab_config['paths']['raw'], front_image)).show()
                cert = input('Enter the PSA certification number: ')
                manual_count += 1

            # if cert != slab_config['default_cert']:
            # write new images to target directory
            front_image_name = '{0}{1}{2}'.format(
                cert,
                slab_config['naming']['front_suffix'],
                slab_config['image_ext'])

            back_image_name = '{0}{1}{2}'.format(
                cert,
                slab_config['naming']['back_suffix'],
                slab_config['image_ext'])

            images = {
                'directories': {
                    'source': slab_config['paths']['raw'],
                    'target': slab_config['paths']['final']
                },
                'images':
                [
                    {
                        'source': {
                            'name': front_image
                        },
                        'target': {
                            'name': front_image_name
                        }
                    },
                    {
                        'source': {
                            'name': image_pair[1]
                        },
                        'target': {
                            'name': back_image_name
                        }
                    }
                ]
            }
            write_target_dir(images)

            composite_image = build_composite_image(image_pair)
            composite_image.save(
                fp='{0}{1}{2}{3}'.format(
                    slab_config['paths']['final'],
                    cert,
                    slab_config['naming']['composite_suffix'],
                    slab_config['image_ext']
                ),
                format='PNG'
            )

            square_image = build_square_image(image_pair)
            square_image.save(
                fp='{0}{1}{2}{3}'.format(
                    slab_config['paths']['final'],
                    cert,
                    slab_config['naming']['square_suffix'],
                    slab_config['image_ext']
                ),
                format='PNG'
            )

            # remove the raw files
            os.remove('{0}{1}'.format(slab_config['paths']['raw'], image_pair[0]))
            os.remove('{0}{1}'.format(slab_config['paths']['raw'], image_pair[1]))
            processed += 1
    else:
        print('Error: uneven file count')

    print('in: {0}'.format(raw_count))
    print('manual: {0}'.format(manual_count))
    print('out: {0}'.format(processed))
