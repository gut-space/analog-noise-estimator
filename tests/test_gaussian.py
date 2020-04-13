import unittest

from noise_estimator import gaussian

class GaussianTest(unittest.TestCase):
    def test_gaussian_results(self):
        results = [
            (0, 0.398942, 0, 1),
            (0.11, 0.396536, 0, 1),
            (0.25, 0.386668, 0 , 1),
            (0.776, 0.295222, 0, 1),
            (1, 0.241971, 0, 1),
            (0.333, 0.075475, 2, 5),
            (0.4231, 0.0810454, 3, 4)
        ]
        for x, y, mean, std in results:
            g = gaussian.gaussian(x, mean, std)
            self.assertAlmostEqual(y, g, 4)

    def test_cdf(self):
        lut = gaussian.cumulative_gaussian_lut()
        self.assertAlmostEqual(lut(0), 0, 3)
        self.assertAlmostEqual(lut(1), 1, 3)
        self.assertAlmostEqual(lut(0.5), 0.5, 1)
