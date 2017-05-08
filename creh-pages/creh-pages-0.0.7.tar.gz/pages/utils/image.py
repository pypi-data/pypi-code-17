from imagekit.processors import ResizeToFill

from .constants import PAGE_SLIDER_SIZES


def get_slider_sizes():
    sizes = []
    for size in PAGE_SLIDER_SIZES:
        sizes.append(ResizeToFill(size[0], size[1]))
    return sizes