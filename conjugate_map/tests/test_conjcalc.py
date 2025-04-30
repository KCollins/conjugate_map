#!/usr/bin/env python
# Full license can be found in License.md
# Full author list can be found in .zenodo.json file
# DOI:10.5281/zenodo.10056623
# ----------------------------------------------------------------------------
"""Integration and unit test suite for conj_calc methods."""

import datetime as dt
import unittest
import importlib.util

import conjugate_map.conj_calc as conj


class TestFindConjugate(unittest.TestCase):
    """Integration and unit test suite for conj_calc methods."""

    def setUp(self):
        """Initialize the test case by copying over necessary files."""
        self.ut = dt.datetime(1980, 11, 3, 18, 0, 0)
        self.lat = 64  # Latitude in degrees (positive for north)
        self.lon = 64  # Longitude in degrees
        self.method = 'geopack'
        self.expected_lat = 0.0
        self.expected_lon = 0.0

    def tearDown(self):
        """Clean up the test environment."""
        del self.ut, self.lat, self.lon, self.method, self.expected_lat
        del self.expected_lon

    def eval_findconj(self):
        """Evaluate the `findconj` function."""
        result_lat, result_lon = conj.findconj(self.lat, self.lon, self.ut,
                                               method=self.method)

        # Assert that the returned values are close enough to expected values
        self.assertAlmostEqual(result_lat, self.expected_lat, delta=1)
        self.assertAlmostEqual(result_lon, self.expected_lon, delta=1)

    def test_geopack_method_north(self):
        """
        Test `findconj` with 'geopack' method for a northern hemisphere point.
        """
        self.ut = dt.datetime(1980, 11, 3, 18, 0, 0)
        self.lat = 88  # Latitude in degrees (positive for north)
        self.lon = 88  # Longitude in degrees
        self.expected_lat = 88.08939422060968
        self.expected_lon = 98.3011528002826

        self.eval_findconj()

    def test_geopack_method_south(self):
        """
        Test `findconj` with 'geopack' method for a southern hemisphere point.
        """
        # Convert location to the southern and western hemispheres
        self.lat *= -1  # Latitude in degrees (negative for south)
        self.lon *= -1  # Longitude in degrees
        self.expected_lat = 39.240006321966526
        self.expected_lon = 291.07394597054764

        self.eval_findconj()

    def test_aacgm_method(self):
        """
        Test `findconj` with 'aacgm' method.
        """
        self.lat *= -1  # Latitude in degrees
        self.expected_lat = 70.57276018835482
        self.expected_lon = 7.938124218080061
        self.method = "aacgm"

        self.eval_findconj()

    def test_auto_method_north(self):
        """
        Test `findconj` with 'auto' method for a northern hemisphere point.
        """
        self.lat = 50  # Latitude in degrees (positive for north)
        self.lon = 0  # Longitude in degrees
        self.method = "auto"

        # Expected method to switch to 'geopack' due to lower latitude
        self.expected_lat = 55.734963905404676
        self.expected_lon = 359.0781222221389

        self.eval_findconj()

    def test_auto_method_south(self):
        """
        Test `findconj` with 'auto' method for a southern hemisphere point.
        """
        self.lat = -88  # Latitude in degrees (negative for south)
        self.lon = 0  # Longitude in degrees
        self.method = "auto"

        # Expected method to switch to 'aacgm' due to higher latitude
        self.expected_lat = 63.10539805333622
        self.expected_lon = -62.838832111320556

        self.eval_findconj()

    def test_qdip_method_south(self):
        """
        Test `findconj` with quasidipole method for a southern hemisphere point.
        """
        self.lat = -88  # Latitude in degrees (negative for south)
        self.lon = 0  # Longitude in degrees
        self.method = "qdip"

        # Output if apexpy is installed:
        if importlib.util.find_spec("apexpy") is not None:
            self.expected_lat = 63.04719543457031
            self.expected_lon = -62.91141891479492
        else:
            # expect to revert to auto
            self.expected_lat = 63.10539805333622
            self.expected_lon = -62.838832111320556

        self.eval_findconj()

    def test_invalid_method(self):
        """
        Test `findconj` with an invalid method.
        """
        self.lat = 45  # Latitude in degrees
        self.lon = 90  # Longitude in degrees
        self.method = 'invalid_method'

        self.eval_findconj()
