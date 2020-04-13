import unittest

import numpy as np
import cv2

from noise_estimator.estimation import estimate_in_boxes, estimate_noise
from noise_estimator.laplacians import L3


class EstimationTest(unittest.TestCase):
    def test_estiation_in_boxes_count(self):
        mask = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]
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
        mask = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]
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
        img = cv2.imread("data/noise-square.png", cv2.IMREAD_GRAYSCALE)
        global_estimation = estimate_noise(img, L3)
        self.assertGreater(global_estimation, 40)

        results = estimate_in_boxes(img, L3)
        for result in results:
            noise = result['noise']
            self.assertGreater(noise, 40)

    def test_good_square(self):
        img = cv2.imread("data/good-square.png", cv2.IMREAD_GRAYSCALE)
        global_estimation = estimate_noise(img, L3)
        self.assertLess(global_estimation, 10)

        results = estimate_in_boxes(img, L3)
        for result in results:
            noise = result['noise']
            self.assertLess(noise, 20)
