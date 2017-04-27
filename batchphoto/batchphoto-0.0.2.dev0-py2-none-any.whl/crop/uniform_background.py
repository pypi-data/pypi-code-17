import numpy as np
from collections import OrderedDict

class UniformBackground(object):
    '''
    Alorithm for detecting the "forground" extents of an object on a mostly
    uniform background. Once those extents are known, crop the image.
    '''
    def __init__(self):
        p = self.parameters = OrderedDict()
        p['Edge Factor'] = 1.5

    def process(self, image):

        edge_mean = np.mean(np.vstack((image[0, :, :], image[-1, :, :],
                                          image[:, 0, :], image[:, -1, :])),
                               axis=0)

        dark_background = edge_mean <= np.asarray([127, 127, 127])
        edge_fac = self.parameters.get('Edge Factor', 1.5)

        if np.all(dark_background):
            threshold = edge_mean + edge_mean*edge_fac
            extents = np.where(np.all(image > threshold, axis=2))
        else:
            threshold = edge_mean - edge_mean*edge_fac/10
            extents = np.where(np.all(image < threshold, axis=2))

        extents = [(min(ax), max(ax)) for ax in extents]

        return image[slice(*extents[0]), slice(*extents[1])]

def test_black_background():
    # make a fake image
    w, h = 512, 512
    image = np.zeros((w, h, 3), dtype=np.uint8)
    image[200:500, 100:200, :] = [200, 50, 30]
    image = image + np.random.randint(0, 30, (w, h, 3)).astype(np.uint8)

    process = UniformBackground()
    proc_image = process.process(image)

    return image, proc_image

def test_white_background():
    # make a fake image
    w, h = 512, 512
    image = np.zeros((w, h, 3), dtype=np.uint8)
    image[:, :, :] = 255
    image[200:500, 100:200, :] = [200, 50, 30]
    image = image - np.random.randint(0, 30, (w, h, 3)).astype(np.uint8)

    process = UniformBackground()
    proc_image = process.process(image)

    return image, proc_image

def test_image():
    import PIL
    path = '../../../test_images/Unedited.jpg'
    path = '../../../test_images/IMG_0005_crop.jpg'
    image = np.asarray(PIL.Image.open(path))

    from scipy import ndimage
    image = ndimage.gaussian_filter(image, sigma=(50, 50, 0), order=0)

    process = UniformBackground()
    process.parameters['Edge Factor'] = 3
    proc_image = process.process(image)

    return image, proc_image

if __name__ == '__main__':
    from matplotlib import pyplot as plt
    image, proc_image = test_image()
    fig, axes = plt.subplots(1, 2)
    axes[0].imshow(image)
    axes[1].imshow(proc_image)
    plt.show()