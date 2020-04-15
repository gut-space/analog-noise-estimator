from .laplacians import L3
from .estimation import estimate_in_boxes
from .metrics import gauss_middle_range_rating

def estimate(I, box=25) -> float:
    '''
    Fast to use estimate noise function. @I is 2D array of grayscale image.
    Input image is splitted into boxes with @box size (in pixels). Estimation
    is performed in each of them and result is reduced into single value in
    range from 0 - image without noise to 1 - completely noisy image.

    Use Laplacian 3x3 kernel, numpy implementation of convolve and normal
    distribution based function for rating.
    '''
    estimation = estimate_in_boxes(I, L3, box=box)
    noises = [e["noise"] for e in estimation]
    return gauss_middle_range_rating(noises)
