#!/usr/bin/env python3
"""
Agent Dashboard Integrity Verifier

This tool cross-checks agent KPIs against raw telemetry, ensures data provenance,
detects metric drift, and generates auditable reports to prevent misleading dashboards.

Bug Fixes:
1. Fixed accuracy KPI to correctly show 'verified' only when difference is <= 5%
2. Fixed rolling mean/std calculations to handle cases where window size > data
"""

import numpy as np
import pandas as pd
import requests
from datetime import datetime

# Constants
VERIFICATION_THRESHOLD = 0.05  # 5% threshold for accuracy verification
ROLLCALC_WINDOW_SIZE = 10  # Default window size for rolling calculations

def fetch_agent_data(agent_id, api_key):
    """Fetch raw telemetry data for an agent from the API."""
    url = f"https://api.agentplatform.com/telemetry/{agent_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def calculate_rolling_stats(data, window_size=ROLLCALC_WINDOW_SIZE):
    """Calculate rolling mean and standard deviation with proper NaN handling."""
    if len(data) < window_size:
        return None, None, "insufficient data for window size"

    rolling_mean = data.rolling(window=window_size).mean()
    rolling_std = data.rolling(window=window_size).std()

    # Handle cases where rolling calculation results in NaN
    rolling_mean = rolling_mean.bfill().ffill()
    rolling_std = rolling_std.bfill().ffill()

    return rolling_mean, rolling_std, "calculated successfully"

def detect_metric_drift(kpi_values, telemetry_values):
    """Detect metric drift between KPI values and telemetry data."""
    if len(kpi_values) != len(telemetry_values):
        raise ValueError("KPI and telemetry data must have the same length")

    differences = [(k - t) / t for k, t in zip(kpi_values, telemetry_values)]
    mean_diff = np.mean(differences)

    # Check if the mean difference exceeds the verification threshold
    is_verified = abs(mean_diff) <= VERIFICATION_THRESHOLD

    return {
        "mean_difference": mean_diff,
        "is_verified": is_verified,
        "verification_threshold": VERIFICATION_THRESHOLD,
        "status": "verified" if is_verified else "unverified"
    }

def generate_report(agent_id, kpi_data, telemetry_data, drift_results):
    """Generate an HTML report of the verification results."""
    report = f"""
    <html>
    <head><title>Agent Dashboard Integrity Report - {agent_id}</title></head>
    <body>
    <h1>Agent Dashboard Integrity Report</h1>
    <h2>Agent ID: {agent_id}</h2>
    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

    <h3>Verification Results</h3>
    <p>Mean Difference: {drift_results['mean_difference']:.2%}</p>
    <p>Status: {drift_results['status']}</p>
    <p>Threshold: {drift_results['verification_threshold']:.1%}</p>

    <h3>Data Comparison</h3>
    <table border="1">
    <tr><th>Metric</th><th>KPI Value</th><th>Telemetry Value</th><th>Difference</th></tr>
    """

    for i, (kpi, tel) in enumerate(zip(kpi_data, telemetry_data)):
        diff = (kpi - tel) / tel
        report += f"""
        <tr>
        <td>Metric {i+1}</td>
        <td>{kpi:.2f}</td>
        <td>{tel:.2f}</td>
        <td>{diff:.2%}</td>
        </tr>
        """

    report += """
    </table>
    </body>
    </html>
    """

    with open(f"report_{agent_id}.html", "w") as f:
        f.write(report)

    print(f"Report generated: report_{agent_id}.html")

def main():
    """Main function to run the integrity verification."""
    # Example usage with mock data for demonstration
    agent_id = "agent_123"

    try:
        # For demonstration, we'll use random KPI data
        np.random.seed(42)
        kpi_data = np.random.rand(10) * 100  # Random KPI values between 0-100

        # Simulate telemetry data with slight variations
        telemetry_values = [val * (1 + np.random.normal(0, 0.02)) for val in kpi_data]

        # Calculate rolling statistics
        rolling_mean, rolling_std, rolling_status = calculate_rolling_stats(
            pd.Series(telemetry_values)
        )

        print(f"Rolling Mean Calculation: {rolling_status}")
        if rolling_mean is not None:
            print(f"Rolling Mean: {rolling_mean.iloc[-1]:.2f}")
            print(f"Rolling Std: {rolling_std.iloc[-1]:.2f}")

        # Detect metric drift
        drift_results = detect_metric_drift(kpi_data, telemetry_values)

        # Generate report
        generate_report(agent_id, kpi_data, telemetry_values, drift_results)

        print("\nVerification Results:")
        print(f"Mean Difference: {drift_results['mean_difference']:.2%}")
        print(f"Status: {drift_results['status']}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()