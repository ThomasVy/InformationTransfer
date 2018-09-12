#!/usr/bin/env python

import os
import ast

import piexif
from PIL import Image


def extract_piexif(fpath):
    '''
    returns a dictionary of 'exif' data stored in the image at fpath
    if image at fpath has no exif section, returns an empty dict
    '''
    img = Image.open(fpath)
    exif_info = img.info.get("exif")
    img.close()

    if exif_info is None:
        return dict()
    else:
        exif_dict = piexif.load(exif_info)
        data = ast.literal_eval(exif_dict["Exif"][piexif.ExifIFD.UserComment])
        return data


if __name__ == '__main__':
    '''Test program entry point'''

    test_data_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'stills')

    test_images = [
        "0_copy_g.jpg",
        "0_copy.jpg",
        "0_g.jpg",
        "0.jpg"
    ]

    for img in test_images:
        fpath = os.path.join(test_data_path, img)
        data = extract_piexif(fpath)
        if data:
            print "lat read from '" + img + "': " + str(data['gps']['lat'])
            print "long read from '" + img + "': " + str(data['gps']['lat'])
        else:
            print "no exif data from '" + img + "'"
