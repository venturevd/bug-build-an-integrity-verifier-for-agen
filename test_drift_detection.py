#!/usr/bin/env python3
"""
Test script for the Agent Dashboard Integrity Verifier

This script tests the fix for the bug where:
1. The accuracy KPI shows as 'verified' even when there's a 4.1% difference
2. Rolling mean/std calculations return 'nan' when window size > data
"""

import unittest
import numpy as np
import pandas as pd
from integrity_verifier import calculate_rolling_stats, detect_metric_drift

class TestIntegrityVerifier(unittest.TestCase):
    def test_rolling_stats_with_insufficient_data(self):
        """Test that rolling stats handle insufficient data correctly."""
        # Test with data smaller than window size
        data = pd.Series([1, 2, 3])
        window_size = 5

        rolling_mean, rolling_std, status = calculate_rolling_stats(data, window_size)

        self.assertIsNone(rolling_mean)
        self.assertIsNone(rolling_std)
        self.assertEqual(status, "insufficient data for window size")

    def test_rolling_stats_with_sufficient_data(self):
        """Test that rolling stats calculate correctly with sufficient data."""
        # Test with data larger than window size
        data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        window_size = 3

        rolling_mean, rolling_std, status = calculate_rolling_stats(data, window_size)

        self.assertIsNotNone(rolling_mean)
        self.assertIsNotNone(rolling_std)
        self.assertEqual(status, "calculated successfully")

        # Check that the last value is calculated correctly
        expected_mean = (7 + 8 + 9) / 3  # Last window
        # The last value should be the mean of the last window
        # For window size 3 on data [7,8,9,10], the last window is [8,9,10]
        expected_mean = (8 + 9 + 10) / 3
        self.assertAlmostEqual(rolling_mean.iloc[-1], expected_mean, places=2)

    def test_drift_detection_within_threshold(self):
        """Test that drift detection correctly identifies values within threshold."""
        kpi_data = [100, 102, 101, 99, 103]
        telemetry_data = [100, 100, 100, 100, 100]  # 0% difference

        results = detect_metric_drift(kpi_data, telemetry_data)

        self.assertTrue(results['is_verified'])
        self.assertEqual(results['status'], 'verified')
        self.assertAlmostEqual(results['mean_difference'], 0.01, places=2)  # 1% difference

    def test_drift_detection_above_threshold(self):
        """Test that drift detection correctly identifies values above threshold."""
        kpi_data = [100, 102, 101, 99, 103]
        telemetry_data = [95, 95, 95, 95, 95]  # ~5% difference

        results = detect_metric_drift(kpi_data, telemetry_data)

        self.assertFalse(results['is_verified'])
        self.assertEqual(results['status'], 'unverified')
        self.assertAlmostEqual(results['mean_difference'], 0.0632, places=2)  # ~6.32% difference

    def test_drift_detection_exactly_at_threshold(self):
        """Test that drift detection correctly handles values exactly at threshold."""
        kpi_data = [100, 100, 100, 100, 100]
        telemetry_data = [95, 95, 95, 95, 95]  # Exactly 5% difference

        results = detect_metric_drift(kpi_data, telemetry_data)

        self.assertFalse(results['is_verified'])
        self.assertEqual(results['status'], 'unverified')
        self.assertAlmostEqual(results['mean_difference'], 0.05, places=2)  # Exactly 5% difference

if __name__ == "__main__":
    unittest.main()