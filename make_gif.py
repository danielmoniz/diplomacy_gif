# -*- coding: utf-8 -*-

import os

from PIL import Image

import imageio

def make_gif(image_dir_path, target_path):
    images = []
    for item in os.listdir(image_dir_path):
        print item
        item_path = os.path.join(image_dir_path, item)
        if os.path.isfile(item_path):
            try:
                # image = Image.open(item_path)
                image = imageio.imread(item_path)
            except IOError:
                print "File called '{}' is not an image.".format(item)
                continue
            images.append(image)

    print len(images)
    imageio.mimsave(target_path, images)

image_dir_path = os.path.join(os.getcwd(), "images/nerds_all_phases")
target_filename = "game.gif"
target_path = os.path.join(image_dir_path, target_filename)
print "image_dir_path:", image_dir_path
print "output gif:", target_path
make_gif(image_dir_path, target_path)
