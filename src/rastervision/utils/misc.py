import imageio
import numpy as np

# HACK - Delete
def color_correct(band):
    min_value, max_value = (np.min(band[np.nonzero(band)]), 2500)#band.max())

    return (np.maximum(((np.minimum(band, max_value) - min_value) / (max_value - min_value)), 0) * 255).astype(np.uint8)


def save_img(im_array, output_path):
    x = np.transpose(im_array, axes=[2, 0, 1])
    r = color_correct(x[0])
    g = color_correct(x[1])
    b = color_correct(x[2])
    a = np.transpose(np.array([r, g, b]), axes=[1, 2, 0])
    imageio.imwrite(output_path, a)

def rescale_to_ubyte8(im_array):
    info = np.iinfo(im_array.dtype)
    im_array = im_array.astype(np.float64) / info.max
    im_array = 255 * im_array
    return im_array.astype(np.uint8)
