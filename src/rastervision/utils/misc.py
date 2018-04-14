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

# def hacky_bytes(im_array):
#     x = np.transpose(im_array, axes=[2, 0, 1])
#     r = color_correct(x[0])
#     g = color_correct(x[1])
#     b = color_correct(x[2])
#     a = np.transpose(np.array([r, g, b]), axes=[1, 2, 0])
#     return a.astype(np.uint8)

def hacky_bytes(im_array, s=False):
    from PIL import Image

    def color_correct(band):
        if not band.any():
             min_value = 0
        else:
             min_value = np.min(band[np.nonzero(band)])

        #min_value = 0
        #max_value = 3000
        max_value = np.max(band)

        a = (np.maximum(((np.minimum(band, max_value) - min_value) / (max_value - min_value)), 0) * 255)
        b = a

        # Brighten
        # brightness = 2
        # b = np.where(b != 0, b + brightness, b)
        # b = np.where(b > 255, 255, b)

        # Gamma Correct
        # 0.01 to 7.99
        gamma = 1.5
        gamma_correction = 1 / gamma
        b = (255 * ((b / 255.0) ** gamma_correction))
        b = np.where(b > 255, 255, b)

        # Contrast
        # contrast = 30.0
        # contrast_factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
        # b = (contrast_factor * (b - 128)) + 128
        # b = np.where(b > 255, 255, b)

        if s:
            return a.astype(np.uint8)
        else:
            return b.astype(np.uint8)

    x = np.transpose(im_array, axes=[2, 0, 1])

    bands = []
    for i in range(0, x.shape[0]):
        bands.append(color_correct(x[i]))

    a = np.transpose(np.array(bands), axes=[1, 2, 0])
    a = a.astype(np.uint8)

    return a

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
