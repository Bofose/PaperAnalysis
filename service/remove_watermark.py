from skimage import io
from pdf2image import convert_from_path
import numpy as np
from PIL import Image
import os
import sys


def select_pixel2(r, g, b):
    if 175 < r < 250 and 175 < g < 250 and 175 < b < 250:
        return True
    else:
        return False


def handle(imgs):
    for i in range(imgs.shape[0]):
        for j in range(imgs.shape[1]):
            if select_pixel2(imgs[i][j][0], imgs[i][j][1], imgs[i][j][2]):
                imgs[i][j][0] = imgs[i][j][1] = imgs[i][j][2] = 255
    return imgs


def remove_marker_data(original_filename, extension , file_name):
    if extension == 'pdf':
        images = convert_from_path('./' + original_filename)
    index = 0
    for img in images:
        index += 1
        img = np.array(img)
        img = handle(img)
        io.imsave('./img' + str(index) + '.jpg', img)

    im_list = []
    for i in range(index):
        index_val = i + 1
        if index_val == 1:
            im1 = Image.open("img1.jpg")
        else:
            image_name = 'img' + str(index_val) + '.jpg'
            im_list.append(Image.open(image_name))
    pdf_filename = file_name
    im1.save(pdf_filename, "PDF", resolution=100.0, save_all=True, append_images=im_list)
    for i in range(index):
        os.remove('img' + str(i + 1) + '.jpg')