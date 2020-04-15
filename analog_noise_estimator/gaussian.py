import numpy as np

def gaussian(x,x0=0,sigma=1):
    '''Numpy implementation of gaussian'''    
    return np.exp(
        -np.power((x - x0) / sigma, 2) / 2
    ) / (np.sqrt(2 * np.pi) * sigma)

def cumulative_gaussian_lut(step:float=0.01, sigma_count:int=3):
    '''
    Cumulative and normalized gaussian Lookup table.

    1. Function creates gaussian with x0 = 0.5 and sigma = 0.5 / 3 in range
       from 0 to 1.
       According to 3 sigma rule 99.7% values are in range from 0 to 1.
    2. Calculates cumulative sum on gaussian
    4. Normalize by max value

    Arguments are in range [0;1) and values are in range [0;1].
    Argument 0 has value 0.

    Parameters
    ==========
    step: float, optional
        Resolution of LUT. The smaller value, the less accuracy you get.
        The bigger value, the more memory you use. 0.01-0.001 should be good.
    sigma_count: int, optional
        What multiple of sigma should the half of width be.
        According the 1 sigma rule in range +- 1 sigma is 68.2% values.
        According the 2 sigma rule in range +- 2 sigma is 95.4% values.
        According the 3 sigma rule in range +- 3 sigma is 99.7% values.
        According the 4 sigma rule in range +- 4 sigma is 99.994% values.
        You may to use this parameter to control value change rate.
        1 sigma - linear, 4 sigma - slow at begin and at end, fast in middle.

    Returns
    =======
    Function for access to approximated value for given argument.
    It accepts argument from range [0;1) (from 0 (inclusive) to 1 (exclusive)).
    Returns 0 ir 1 if index out of bounds.
    Return the nearest precalculated for given argument (range (0; 1]
    from 0 (exclusive) to 1 (exclusive))).

    Examples
    ========
    >>> lut = cumulative_reversed_gaussian_lut()
    >>> lut(0)
        0
    >>> lut(0.5)
        0.49881326466597947
    >>> lut(0.25)
        0.9339886741945999
    '''
    a = np.arange(0, 1, step)
    width = 1
    half_width = width / 2
    x0 = half_width
    sigma = half_width / sigma_count

    gx = gaussian(a, x0=x0, sigma=sigma)
    cs = np.cumsum(gx)
    max_ = cs[len(cs) - 1]
    normalized_cs = cs / max_

    def get_value(x):
        if x < 0:
            return 0
        elif x >= 1:
            return 1
        idx = int(x / step)
        return normalized_cs[idx]
    return get_value

if __name__ == '__main__':
    # Example usage. Draw gaussian plots and cumulative, normalized
    # plots for different sigma.
    
    step = 0.001
    lut_count = 4
    r = range(1, lut_count + 1)
    luts = [cumulative_gaussian_lut(step=step, sigma_count=i)
                for i in r]
    a = [i * step for i in range(0, int(1 / step))]

    from matplotlib import pyplot as plt
    plt.subplot(1, 2, 1)
    for lut in luts:
        plt.plot(a, [lut(i) for i in a])
    plt.legend(["%d sigma" % (i,) for i in r])

    plt.subplot(1, 2, 2)
    for i in range(1, lut_count + 1):
        sigma = 1 / i
        g = gaussian(np.array(a), 0.5, sigma)
        max_ = g.max()
        g = g / max_
        plt.plot(a, g)
    plt.legend(["%d sigma" % (i,) for i in r])
    plt.suptitle(('Cumulative, normalized gaussian'))
    plt.show()

