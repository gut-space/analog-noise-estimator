from .gaussian import cumulative_gaussian_lut

# Precomputed values of cumulative, normalized Gaussian distribution.
lut = cumulative_gaussian_lut()
def gaussian_rating(noise):
    '''
    Rate quality of region based on Gauss sigma noise value. Empirically
    determinated based on NOAA imageries received by amateur ground station.
    Rate is in range from 0 - good quality to 1 - bad quality.

    If sigma noise is less then 10 then region has good qualty (0).
    If sigma is equal or greater then 20 then region has bad quality (1).
    If sigma is between 10 and 20 then quality is in range 0 to 1. We use normal
    distribution to get this value. For sigma 15 the quality is 0.5. The values
    change faster at the ends of the interval and slower at the middle value.
    The rationale is that 10-12 are quite good, 15 is average and 18-20 are bad.
    Noise is natural, random process then normal distribution should good
    descirbe it.
    '''
    if noise < 10:
        return 0
    if noise < 20:
        normalized = (noise - 10) / 10
        return lut(normalized)
    return 1