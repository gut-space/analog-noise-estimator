'''
Module for estimate analog noise on the images.

Contains implementation of paper:
J. Immerkær, “Fast Noise Variance Estimation”, Computer Vision and Image
Understanding, Vol. 64, No. 2, pp. 300-302, Sep. 1996

You can estimate noise in whole image (as in original idea) just using
@estimate_noise function or estimate noise in small boxes separately using 
@estimate_in_boxes and next merge estimations into single result (for example
using @rating function).
merge
'''
import math

import numpy as np
from numpy.fft  import fft2, ifft2

def np_fftconvolve(A, B):
    '''
    Convolve 2D implementation in Numpy. Doesn't produce the same result 
    as scipy.signal.convolve2d function, but results are close (<1% difference).
    See: https://laurentperrinet.github.io/sciblog/posts/2017-09-20-the-fastest-2d-convolution-in-the-world.html
    As described above it should be fastest method (in 2017), but in my opinion
    it is slower then Scipy solution.
    '''
    return np.real(ifft2(fft2(A)*fft2(B, s=A.shape)))

def estimate_noise(I, L, conv2d=np_fftconvolve):
    '''
    Estimate the variance of additive zero mean Gaussian noise .
    See: https://stackoverflow.com/a/25436112
    Reference: J. Immerkær, “Fast Noise Variance Estimation”, Computer Vision
        and Image Understanding, Vol. 64, No. 2, pp. 300-302, Sep. 1996

    Parameters
    ==========
    I : 2D array
        Input, greyscale image
    L : List of list of integers
        Mask, should be smaller then image (best 3x3)
    conv2d : function
        Convolve 2D implementation to use. Accept 2D array and 2D mask,
        returns new 2D array.
    '''
    L = np.array(L)

    # This is a fix for handling images read by imread from matplotlib.pyplot. Its shape
    # returns a tuple of 3 elements, instead of two as opencv's imread does. We don't care
    # about the third parameter, but we don't want python to freak out that we unpack too few
    # variables.
    H, W, *_ = I.shape
    Lh, Lw = L.shape
    LhalfH = math.ceil(Lh / 2)
    LhalfW = math.ceil(Lw / 2)

    matrix_factor = math.sqrt(np.sum(np.power(L.flatten(), 2)))
    sigma = np.sum(np.sum(np.absolute(conv2d(I, L))))
    sigma = sigma * math.sqrt(0.5 * math.pi) / (matrix_factor * (W-LhalfW) * (H-LhalfH))

    return sigma

def estimate_in_boxes(I, L, conv2d=np_fftconvolve, box=25):
    '''
    Split input I image and boxes with @box size (in pixels) and perform
    estimation in each.
    Returns list of dictionaries with 'row' and 'col'  coordinates of left, upper
    pixel of box and 'noise' with estimated noise sigma value (sigma from Gauss
    distribution of noise).
    '''

    # This is a fix for handling images read by imread from matplotlib.pyplot. Its shape
    # returns a tuple of 3 elements, instead of two as opencv's imread does. We don't care
    # about the third parameter, but we don't want python to freak out that we unpack too few
    # variables.
    rows, cols, *_ = I.shape
    results = []
    for rowIdx in range(0, rows, box):
        for colIdx in range(0, cols, box):
            subimage = I[rowIdx:rowIdx+box, colIdx:colIdx+box]
            noise = estimate_noise(subimage, L, conv2d)
            results.append({
                'row': rowIdx,
                'col': colIdx,
                'noise': noise
            })
    return results
