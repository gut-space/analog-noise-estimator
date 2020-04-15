import unittest

import numpy as np

from analog_noise_estimator.estimation import np_fftconvolve

class ConvolveTest(unittest.TestCase):
    def test_empty(self):
        mask = [[0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]]
        I = [[0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0]]
        mask = np.array(mask)
        I = np.array(I)
        output = np_fftconvolve(I, mask)
        self.assertTrue((I == output).all())

    def test_simply_mask(self):
        mask = [[-1,  0,  1],
                [ 0,  5,  0],
                [ 1,  0, -1]]
        I = [[1, 2, 1, 2, 1, 2],
             [2, 1, 2, 1, 2, 1],
             [1, 2, 1, 2, 1, 2],
             [2, 1, 2, 1, 2, 1],
             [1, 2, 1, 2, 1, 2],
             [2, 1, 2, 1, 2, 1]]

        mask = np.array(mask)
        I = np.array(I)
        output = np_fftconvolve(I, mask)
        count = 0
        for row_idx, row in enumerate(output):
            for val_idx, val in enumerate(row):
                exp = 5 if row_idx % 2 == 0 and \
                            val_idx % 2 == 0 or \
                           row_idx % 2 == 1 and \
                            val_idx % 2 == 1 else 10
                count += 1
                self.assertAlmostEqual(exp, val, 7)
        self.assertEqual(count, I.size)