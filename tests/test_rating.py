import unittest

from noise_estimator.rating import gaussian_rating

class RatingTest(unittest.TestCase):
    
    def test_gaussian_rating(self):
        for i in range(0, 10):
            self.assertEqual(gaussian_rating(i), 0)
        previous_rate = 0
        for i in range(10, 20):
            rate = gaussian_rating(i)
            self.assertGreaterEqual(rate, 0)
            self.assertLessEqual(rate, 1)
            self.assertGreaterEqual(rate, previous_rate)
            previous_rate = rate
        for i in range(20, 50):
            self.assertEqual(gaussian_rating(i), 1) 