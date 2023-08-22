import unittest

import numpy as np
import os

from analog_noise_estimator.estimation import estimate_in_boxes, estimate_noise
from analog_noise_estimator.laplacians import L3


class EstimationTest(unittest.TestCase):
    def get_data_dir(self):
        """
        Returns the directory where this py file is located. The assumption is
        that the test npy files will be in the same location. This is
        important, if the sources are included in other project (such as Svarog)
        """
        dir, _ = os.path.split(__file__)
        return dir + os.path.sep

    def test_estiation_in_boxes_count(self):
        mask = L3
        I = [[0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0]]

        mask = np.array(mask)
        I = np.array(I)

        results = estimate_in_boxes(I, mask, box=5)
        self.assertEqual(len(results), 4)

        results = estimate_in_boxes(I, mask, box=8)
        self.assertEqual(len(results), 1)

    def test_estiation_in_boxes_coordinates(self):
        mask = L3
        I = [[0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0]]

        mask = np.array(mask)
        I = np.array(I)

        results = estimate_in_boxes(I, mask, box=5)

        actual = set((r['row'], r['col']) for r in results)
        expected = set([(0, 0), (0, 5), (5, 0), (5, 5)])
        self.assertEqual(actual, expected)

    def test_noisy_square(self):
        img = np.load(self.get_data_dir() + "noisy.npy")
        global_estimation = estimate_noise(img, L3)
        self.assertGreater(global_estimation, 40)

        results = estimate_in_boxes(img, L3)
        for result in results:
            noise = result['noise']
            self.assertGreater(noise, 40)

    def test_good_square(self):
        img = np.load(self.get_data_dir() + "good.npy")
        global_estimation = estimate_noise(img, L3)
        self.assertLess(global_estimation, 10)

        results = estimate_in_boxes(img, L3)
        for result in results:
            noise = result['noise']
            self.assertLess(noise, 20)
