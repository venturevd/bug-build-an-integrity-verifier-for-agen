# Changes Made to Fix the 'nan' Issue in Rolling Mean/Std Calculation

## Problem
The drift detection in the Agent Dashboard Integrity Verifier was showing 'nan' values for rolling mean and standard deviation, which suggested an issue with the rolling window calculation.

## Root Cause
The issue occurred when the rolling window size was larger than the available data. In such cases, the rolling mean and standard deviation calculations would return NaN values, which were then directly used in the report generation without proper handling.

## Solution
1. **Fixed the `detect_metric_drift` function**:
   - Added proper handling for NaN values in rolling calculations
   - When the window size is larger than the data, the function now returns None for mean/std and indicates "insufficient data for window size"
   - Added proper checks before calculating control limits and outliers

2. **Updated the report generation**:
   - Modified the HTML report template to handle None values for mean/std
   - Changed display from 'nan' to 'N/A' for better readability
   - Added proper status messaging for insufficient data cases

## Files Modified
- `integrity_verifier.py`: Fixed the rolling calculation logic and report generation
- `README.md`: Added documentation about the bug fix

## Testing
- Created a comprehensive test script (`test_drift_detection.py`) to verify the fix
- Tested with various window sizes (larger, equal, and smaller than data)
- Verified that the report now correctly handles edge cases

## Results
The tool now properly handles cases where there's insufficient data for the rolling window, displaying 'N/A' instead of 'nan' and providing clear status messages about the data adequacy for analysis.