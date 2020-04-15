'''
Functions to reduce sigma noise series to single value in [0, 1) range
'''
from .rating import gaussian_rating

def average_sigma(noises):
    return sum(noises) / len(noises)

def average_sigma_clip(noises, clip_sigma=30):
    return sum(min(n, clip_sigma) for n in noises) / len(noises)

def constant_ranges_rating(noises):
    return sum(0 if n < 10 else 0.5 if n < 20 else 1 for n in noises) / len(noises)

def linear_middle_range_rating(noises):
    return sum(0 if n < 10 else (n - 10) / 10 if n < 20 else 1 for n in noises) / len(noises)

def gauss_middle_range_rating(noises):
    return sum(gaussian_rating(n) for n in noises) / len(noises)