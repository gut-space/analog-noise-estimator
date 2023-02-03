import unittest
import os

import numpy

from analog_noise_estimator.main import estimate

class MainTest(unittest.TestCase):

    def get_data_dir(self):
        """
        Returns the directory where this py file is located. The assumption is
        that the test npy files will be in the same location. This is
        important, if the sources are included in other project (such as Svarog)
        """
        dir, _ = os.path.split(__file__)
        return dir + os.path.sep


    def test_good_square(self):
        img = numpy.load(self.get_data_dir() + "good.npy")
        rate = estimate(img)
        self.assertLess(rate, 0.1)

    def test_noisy_square(self):
        img = numpy.load(self.get_data_dir() + "noisy.npy")
        rate = estimate(img)
        self.assertGreater(rate, 0.99)
