"""Integration and unit test suite for conj_calc methods."""
#!/usr/bin/env python
# Full license can be found in License.md
# Full author list can be found in .zenodo.json file
# DOI:10.5281/zenodo.10056623
# ----------------------------------------------------------------------------

import datetime as dt
import unittest

import conjugate_map.conj_calc as conj

class TestFindConjugate(unittest.TestCase):
    """Integration and unit test suite for conj_calc methods."""
    def test_geopack_method_north(self):
        """
        Test `findconj` with 'geopack' method for a northern hemisphere point.
        """
        ut = dt.datetime(1980, 11, 3, 18, 0, 0)
        lat = 64  # Latitude in degrees (positive for north)
        lon = 64  # Longitude in degrees
        expected_lat, expected_lon = 65.38287134065757, 65.63983817802247

        result_lat, result_lon = conj.findconj(lat, lon, ut, method='geopack')

        # Assert that the returned values are close enough to expected values
        self.assertAlmostEqual(result_lat, expected_lat, delta=1)
        self.assertAlmostEqual(result_lon, expected_lon, delta=1)

    def test_geopack_method_south(self):
        """
        Test `findconj` with 'geopack' method for a southern hemisphere point.
        """
        ut = dt.datetime(1980, 11, 3, 18, 0, 0)
        lat = -64  # Latitude in degrees (negative for south)
        lon = -64  # Longitude in degrees
        expected_lat, expected_lon = 39.240006321966526, 291.07394597054764

        result_lat, result_lon = conj.findconj(lat, lon, ut, method='geopack')

        # Assert that the returned values are close enough to expected values
        self.assertAlmostEqual(result_lat, expected_lat, delta=1)
        self.assertAlmostEqual(result_lon, expected_lon, delta=1)

    def test_aacgm_method(self):
        """
        Test `findconj` with 'aacgm' method.
        """
        ut = dt.datetime(1980, 11, 3, 18, 0, 0)
        lat = -64  # Latitude in degrees
        lon = 64  # Longitude in degrees
        expected_lat, expected_lon = 70.57276018835482, 7.938124218080061

        result_lat, result_lon = conj.findconj(lat, lon, ut, method='aacgm')

        # Assert that the returned values are close enough to expected values
        self.assertAlmostEqual(result_lat, expected_lat, delta=1)
        self.assertAlmostEqual(result_lon, expected_lon, delta=1)

    def test_auto_method_north(self):
        """
        Test `findconj` with 'auto' method for a northern hemisphere point.
        """
        ut = dt.datetime(1980, 11, 3, 18, 0, 0)
        lat = 50  # Latitude in degrees (positive for north)
        lon = 0  # Longitude in degrees
        # Expected method to switch to 'geopack' due to lower latitude
        expected_lat, expected_lon = 55.734963905404676, 359.0781222221389
        result_lat, result_lon = conj.findconj(lat, lon, ut, method='auto')

        self.assertAlmostEqual(result_lat, expected_lat, delta=1)
        self.assertAlmostEqual(result_lon, expected_lon, delta=1)

    def test_auto_method_south(self):
        """
        Test `findconj` with 'auto' method for a southern hemisphere point.
        """
        ut = dt.datetime(1980, 11, 3, 18, 0, 0)
        lat = -88  # Latitude in degrees (negative for south)
        lon = 0  # Longitude in degrees
        # Expected method to switch to 'aacgm' due to higher latitude

        expected_lat, expected_lon = 63.10539805333622, -62.838832111320556
        result_lat, result_lon = conj.findconj(lat, lon, ut, method='auto')

        self.assertAlmostEqual(result_lat, expected_lat, delta=1)
        self.assertAlmostEqual(result_lon, expected_lon, delta=1)

    def test_invalid_method(self):
        """
        Test `findconj` with an invalid method.
        """
        ut = dt.datetime(1980, 11, 3, 18, 0, 0)
        lat = 45  # Latitude in degrees
        lon = 90  # Longitude in degrees
        expected_lat, expected_lon = 0, 0  # Expect default values

        result_lat, result_lon = conj.findconj(lat, lon, ut, method='invalid_method')

        self.assertEqual(result_lat, expected_lat)
        self.assertEqual(result_lon, expected_lon)
