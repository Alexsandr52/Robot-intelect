"""CPU-only checks for the AEL-75 sustained contact criterion."""

import unittest

from scripts.ael75_g1_box_scene import sustained_contact_samples


class SustainedContactSamplesTest(unittest.TestCase):
    def test_single_impulse_does_not_fill_the_trailing_window(self):
        above_threshold, window_size = sustained_contact_samples([0.0] * 59 + [2.0], 0.981, 60)

        self.assertEqual((above_threshold, window_size), (1, 60))
        self.assertLess(above_threshold / window_size, 0.9)

    def test_stable_contact_fills_the_trailing_window(self):
        above_threshold, window_size = sustained_contact_samples([2.0] * 60, 0.981, 60)

        self.assertEqual((above_threshold, window_size), (60, 60))
        self.assertGreaterEqual(above_threshold / window_size, 0.9)

    def test_incomplete_window_is_rejected(self):
        with self.assertRaises(ValueError):
            sustained_contact_samples([2.0] * 59, 0.981, 60)


if __name__ == "__main__":
    unittest.main()
