# Analog noise estimation

Module for estimate analog noise on the images.

Contains implementation of paper:
J. Immerkær, “Fast Noise Variance Estimation”, Computer Vision and Image
Understanding, Vol. 64, No. 2, pp. 300-302, Sep. 1996

You can estimate noise in whole image (as in original idea) or estimate noise
in small boxes  and next merge estimations into single result using provided
rating functions.

For examples and results see [analog-noise-estimator-cli](https://github.com/gut-space/analog-noise-estimator-cli) on Github.

# How to use

## Quick path

```python
import cv2
import analog_noise_estimator

img = cv2.imread("data/product.png", cv2.IMREAD_GRAYSCALE)

noise = analog_noise_estimator.estimate(img)

print("Noisy / all", noise)
```

## Complex example

```python
import cv2
from analog_noise_estimator.rating import gaussian_rating as rating
from analog_noise_estimator.estimation import np_fftconvolve, estimate_in_boxes, estimate_noise
from analog_noise_estimator import laplacians
from analog_noise_estimator import metrics

img = cv2.imread("data/product.png", cv2.IMREAD_GRAYSCALE)

L = laplacians.L3

# Global recognition
sigma = estimate_noise(img, L)

# Local recognition
noise_stats = estimate_in_boxes(img, L, 25)
noises = [s['noise'] for s in noise_stats]

# Sigma - Gauss distribution parameter for describe 'size' ('area') of the noise)
# Global value of sigma for whole image:
print("Global sigma:", sigma)
# Average of sigma in separate boxes
print("Average local sigma:", metrics.average_sigma(noises))
# Average of sigma in separate boxes, but sigma is cliped to 30.
print("Average local sigma clip:", metrics.average_sigma_clip(noises, 30))
# Rating calculated on global sigma
print("Global rating:", rating(sigma))
# Rating with constant threshold. 0 for sigma < 10, 0.5 for sigma < 20 otherwise 1.
print("Constant metric:", metrics.constant_ranges_rating(noises))
# Rating with linear value for sigma between 10 and 20.
print("Linear metric:", metrics.linear_middle_range_rating(noises))
# Rating based on normal distribution for sigma between 10 and 20.
print("Gauss metric:", metrics.gauss_middle_range_rating(noises))
```
# Gauss rating

This package contains function for rate noise. It returns 0 for good quality image and 1 for noisy. Rating is based on detected sigma value.

We assume that sigma less then 10 means clear image (rate 0). Different sensors may to produce different average sigma. But empirical analysis has shown that good quality images have sigma 10 or less.

Sigma greater then 20 means that image is bad (rate 1).

Values between 10 and 20 are problematic. 11-12 are quite code, 17-19 are quite bad, 13-16 are medium, but the relationship does not seem to be linear. We use cumulative (normalized) normal distribution function for determining this value.

# References

J. Immerkær, “Fast Noise Variance Estimation”, Computer Vision and Image Understanding, Vol. 64, No. 2, pp. 300-302, Sep. 1996
