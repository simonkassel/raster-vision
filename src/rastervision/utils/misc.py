import imageio
import numpy as np

# HACK
def color_correct(band):
        # if not band.any():
        #     min_value = 0
        # else:
        #     min_value = np.min(band[np.nonzero(band)])

        min_value = 0
        max_value = 1800

        return (np.maximum(((np.minimum(band, max_value) - min_value) / (max_value - min_value)), 0) * 255).astype(np.uint8)

def hacky_bytes(im_array):
    x = np.transpose(im_array, axes=[2, 0, 1])
    r = color_correct(x[0])
    g = color_correct(x[1])
    b = color_correct(x[2])
    a = np.transpose(np.array([r, g, b]), axes=[1, 2, 0])
    return a.astype(np.uint8)

def save_img(im_array, output_path, c=True):
    if c:
        a = hacky_bytes(im_array)
        imageio.imwrite(output_path, a)
    else:
        imageio.imwrite(output_path, im_array)

# def save_img(im_array, output_path, c=True):
#     if im_array.dtype == np.uint8:
#         imageio.imwrite(output_path, im_array)
#     else:
#         import os
#         op = os.path.splitext(output_path)[0] + '.bmp'
#         imageio.imwrite(op, im_array)

def rescale_to_ubyte8(im_array):
    info = np.iinfo(im_array.dtype)
    im_array = im_array.astype(np.float64) / info.max
    im_array = 255 * im_array
    return im_array.astype(np.uint8)
