import unittest

import cv2

from noise_estimator.main import estimate

class MainTest(unittest.TestCase):

    def test_good_square(self):
        img = cv2.imread("data/good-square.png", cv2.IMREAD_GRAYSCALE)
        rate = estimate(img)
        self.assertLess(rate, 0.1)

    def test_noisy_square(self):
        img = cv2.imread("data/noise-square.png", cv2.IMREAD_GRAYSCALE)
        rate = estimate(img)
        self.assertGreater(rate, 0.99)

        