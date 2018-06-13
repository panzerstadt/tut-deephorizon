from flask import Flask

import Algorithmia

import base64
import math
from PIL import Image
import os

from hidden import API_KEY


def find_horizon(file_in):
    algo = client.algo('ukyvision/deephorizon/0.1.0')
    image = base64.b64encode(open(file_in, "rb").read())
    image_encoded = 'data:image/jpg;base64' + str(image)
    image_encoded = image_encoded.replace('base64b', 'base64,')  # crappy hack
    print(image_encoded)
    return algo.pipe({
        'image': image_encoded
    }).result


def calculate_rotation(coords):
    """
    :param coords: {left: [x1,y1], right: [x2,y2]}
    :return: rotation, in degrees
    """
    (x1, y1) = coords['left']
    (x2, y2) = coords['right']
    slope = (y2-y1)/(x2-x1)
    return math.degrees(math.atan(slope))


def rotate_image(file_in, file_out, degrees, crop):
    """
    rotate an image by a number fo degrees, crop if desired, save to file_out
    :param file_in:
    :param file_out:
    :param degrees:
    :param crop:
    :return:
    """
    Image.open(file_in).rotate(degrees, expand=not crop, resample=Image.BILINEAR).save(file_out)


client = Algorithmia.Client(API_KEY)
folder = './images'

img_list = list(os.walk(folder))[0]
image_list = [os.path.join(img_list[0], x) for x in img_list[2]]


def correct_horizon(image_filepath_in):
    """
    :param image_filepath_in: filepath of image. jpegs only please!
    :return:
    """
    file_in = image_filepath_in
    file_out = os.path.splitext(image_filepath_in)[0] + '_out.jpeg'
    line = find_horizon(file_in)
    rotation = calculate_rotation(line)
    rotate_image(file_in, file_out, -rotation, True)


def correct_horizons(image_filepath_list):
    for image in image_filepath_list:
        correct_horizon(image)
        print('corrected: '+ image)
    print('complete!')
    return True

correct_horizons(image_list)