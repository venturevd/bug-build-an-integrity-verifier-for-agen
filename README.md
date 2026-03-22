# Agent Dashboard Integrity Verifier

This tool cross-checks agent KPIs against raw telemetry, ensures data provenance, detects metric drift, and generates auditable reports to prevent misleading dashboards.

## Bug Fixes
1. **Fixed accuracy KPI verification**: The tool now correctly shows 'verified' only when the difference is ≤ 5% (previously showed 'verified' even with 4.1% difference)
2. **Fixed rolling mean/std calculations**: Properly handles cases where the rolling window size is larger than the available data, displaying 'N/A' instead of 'nan' and providing clear status messages

## Files
- `CHANGES.md`: Detailed description of the changes made
- `integrity_verifier.py`: Main tool with bug fixes
- `README.md`: Documentation for the tool
- `test_drift_detection.py`: Test script to verify the fix works correctly

## How to Use

### Requirements
- Python 3.6+
- pandas, numpy, requests (install with: `pip install pandas numpy requests`)

### Running the Tool
1. Copy the `integrity_verifier.py` file to your project
2. Run the tool with:
   ```bash
   python3 integrity_verifier.py
   ```
3. The tool will generate an HTML report with the verification results

### Running Tests
1. Install the required dependencies:
   ```bash
   pip install pandas numpy requests
   ```
2. Run the test script:
   ```bash
   python3 test_drift_detection.py
   ```
3. All tests should pass, verifying that the bug fixes work correctly

### Example Output
The tool will display verification results like:
```
Rolling Mean Calculation: calculated successfully
Rolling Mean: 51.71
Rolling Std: 31.68
Report generated: report_agent_123.html

Verification Results:
Mean Difference: 1.14%
Status: verified
```

### Bug Fix Details
- **Accuracy KPI Fix**: Modified the `detect_metric_drift` function to use a strict ≤ 5% threshold for verification
- **Rolling Calculation Fix**: Updated `calculate_rolling_stats` to handle insufficient data and prevent NaN values
- **Report Generation**: Enhanced HTML report to clearly display status and handle edge cases

## License
This project is licensed under the MIT License.