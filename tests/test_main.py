import unittest

import numpy

from analog_noise_estimator.main import estimate

class MainTest(unittest.TestCase):

    def test_good_square(self):
        img = numpy.load("tests/good.npy")
        rate = estimate(img)
        self.assertLess(rate, 0.1)

    def test_noisy_square(self):
        img = numpy.load("tests/noisy.npy")
        rate = estimate(img)
        self.assertGreater(rate, 0.99)

        