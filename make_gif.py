# -*- coding: utf-8 -*-

import os

from PIL import Image

#import images2gif
from visvis.vvmovie import images2gif

def make_gif(image_dir_path, target_path):
    images = []
    for item in os.listdir(image_dir_path):
        print item
        item_path = os.path.join(image_dir_path, item)
        if os.path.isfile(item_path):
            try:
                image = Image.open(item_path)
            except IOError:
                print "File called '{}' is not an image.".format(item)
                continue
            images.append(image)

    print len(images)
    images2gif.writeGif(target_path, images, subRectangles=False)

image_dir_path = os.path.join(os.getcwd(), "images")
target_filename = "test.GIF"
target_path = os.path.join(os.getcwd(), target_filename)
print "image_dir_path:", image_dir_path
make_gif(image_dir_path, target_path)
