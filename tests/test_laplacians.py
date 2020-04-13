import unittest

from noise_estimator import laplacians

class LaplaciansTest(unittest.TestCase):
    def test_elements_sum(self):
        matrixes = [laplacians.L3, laplacians.L5, laplacians.L7]
        for matrix in matrixes:
            acc = 0
            for row in matrix:
                for val in row:
                    acc += val
            self.assertEqual(acc, 0)