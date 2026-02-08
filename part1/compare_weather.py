import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_squared_error
import os
import sys


print("loading...")

# check if all required files exist
required_files = ['era5_data.nc', 'IFS_forecast_europe.nc', 'AIFS_forecast_europe.nc']
for file in required_files:
    if not os.path.exists(file):
        print(f"ERROR: Required file '{file}' not found!")
        sys.exit(1)

try:
    era5 = xr.open_dataset('era5_data.nc')
    ifs = xr.open_dataset('IFS_forecast_europe.nc')
    aifs = xr.open_dataset('AIFS_forecast_europe.nc')
except Exception as e:
    print(f"ERROR: Failed to load datasets: {e}")
    sys.exit(1)

# check if era5 data file uses valid time or time and change to time if necessary
if 'valid_time' in era5.coords:
    era5 = era5.rename({'valid_time': 'time'})

# same thing but for temperrature variable
if '2t' in era5.data_vars:
    era5 = era5.rename({'2t': 't2m'})

# check if required variables exist
if 't2m' not in era5.data_vars:
    print("ERROR: Temperature variable 't2m' not found in ERA5 data!")
    print(f"Available variables: {list(era5.data_vars)}")
    sys.exit(1)

if 't2m' not in ifs.data_vars:
    print("ERROR: Temperature variable 't2m' not found in IFS data!")
    print(f"Available variables: {list(ifs.data_vars)}")
    sys.exit(1)

if 't2m' not in aifs.data_vars:
    print("ERROR: Temperature variable 't2m' not found in AIFS data!")
    print(f"Available variables: {list(aifs.data_vars)}")
    sys.exit(1)

# finding common times
common_times = np.intersect1d(era5.time, ifs.time)

if len(common_times) == 0:
    print("ERROR: No matching times found between ERA5 and IFS datasets!")
    print(f"  ERA5 times: {era5.time.values}")
    print(f"  IFS times: {ifs.time.values}")
    sys.exit(1)

print(f"analyzing {len(common_times)} common time steps.")

# filter to matching times
era5_sub = era5.sel(time=common_times)
ifs_sub = ifs.sel(time=common_times)
aifs_sub = aifs.sel(time=common_times)

# aligning the grids
# interpolate the forecasts onto the ERA5 grid 
print("aligning forecast grids to ERA5 data...")
ifs_aligned = ifs_sub.interp_like(era5_sub, method='linear')
aifs_aligned = aifs_sub.interp_like(era5_sub, method='linear')

# define metric functions
def compute_metrics(forecast_da, truth_da, times):
    mae_list = []
    rmse_list = []
    r2_list = []

    print(f"computing metrics for {forecast_da.name}...")
    
    for t in times:
        # extract the 2D slice for this time
        f_slice = forecast_da.sel(time=t).values.flatten()
        gt_slice = truth_da.sel(time=t).values.flatten()
        
        # Remove NaNs (e.g., if one map masks the ocean and the other doesn't)
        mask = ~np.isnan(gt_slice) & ~np.isnan(f_slice)
        f_clean = f_slice[mask]
        gt_clean = gt_slice[mask]

        # calculate Metrics
        mae = np.mean(np.abs(f_clean - gt_clean))
        rmse = np.sqrt(mean_squared_error(gt_clean, f_clean))
        r2 = r2_score(gt_clean, f_clean)
        
        mae_list.append(mae)
        rmse_list.append(rmse)
        r2_list.append(r2)
        
    return mae_list, rmse_list, r2_list

# calculate with aligned data and eras data
ifs_mae, ifs_rmse, ifs_r2 = compute_metrics(ifs_aligned['t2m'], era5_sub['t2m'], common_times)
aifs_mae, aifs_rmse, aifs_r2 = compute_metrics(aifs_aligned['t2m'], era5_sub['t2m'], common_times)

# plot
fig, ax = plt.subplots(3, 1, figsize=(10, 15), sharex=True)

# MAE
ax[0].plot(common_times, ifs_mae, label='IFS', color='blue', marker='o')
ax[0].plot(common_times, aifs_mae, label='AIFS', color='red', marker='x')
ax[0].set_ylabel('MAE (Kelvin)')
ax[0].set_title('Forecast Error Metrics vs ERA5 Ground Truth')
ax[0].legend()
ax[0].grid(True)

# RMSE
ax[1].plot(common_times, ifs_rmse, label='IFS', color='blue', marker='o')
ax[1].plot(common_times, aifs_rmse, label='AIFS', color='red', marker='x')
ax[1].set_ylabel('RMSE (Kelvin)')
ax[1].grid(True)

# R2
ax[2].plot(common_times, ifs_r2, label='IFS', color='blue', marker='o')
ax[2].plot(common_times, aifs_r2, label='AIFS', color='red', marker='x')
ax[2].set_ylabel('R² Score')
ax[2].set_xlabel('Forecast Valid Time')
ax[2].grid(True)

plt.tight_layout()
plt.savefig('part1_results.png')
print("Done! Plot saved to part1_results.png")