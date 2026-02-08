import xarray as xr
import numpy as np
import os
import sys

# 1. Open the two forecast files
# (Make sure these files are in the same folder as your script)
required_files = ['IFS_forecast_europe.nc', 'AIFS_forecast_europe.nc']
for file in required_files:
    if not os.path.exists(file):
        print(f"ERROR: Required file '{file}' not found!")
        sys.exit(1)

try:
    ds1 = xr.open_dataset('IFS_forecast_europe.nc')
    ds2 = xr.open_dataset('AIFS_forecast_europe.nc')
except Exception as e:
    print(f"ERROR: Failed to load datasets: {e}")
    sys.exit(1)

# 2. Extract the time coordinates
# NetCDF files usually call this coordinate 'time' or 'valid_time'
# xarray handles this automatically if you use .time
times1 = ds1.time.values
times2 = ds2.time.values

print(f"File 1 has {len(times1)} time steps.")
print(f"File 2 has {len(times2)} time steps.")

# 3. Find the intersection (matching times)
# This finds values that exist in BOTH arrays
matching_times = np.intersect1d(times1, times2)

if len(matching_times) == 0:
    print("\nERROR: No matching times found between the two datasets!")
    print(f"File 1 times: {times1}")
    print(f"File 2 times: {times2}")
    sys.exit(1)

print(f"\nFound {len(matching_times)} matching times!")
print("-" * 30)
print(matching_times)

output_filename = "matching_times.txt"

# Convert the numpy array of times to strings and save
np.savetxt(output_filename, matching_times, fmt='%s')

print(f"Saved matching times to: {output_filename}")