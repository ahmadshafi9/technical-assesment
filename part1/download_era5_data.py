import cdsapi
import os
import sys

dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": ["2m_temperature"],
    "year": ["2026"],
    "month": ["01"],
    "day": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12",
        "13", "14", "15",
        "16"
    ],
    "time": [
        "00:00", "06:00", "12:00",
        "18:00"
    ],
    "data_format": "netcdf",
    "download_format": "unarchived",
    "area": [75, -25, 30, 45]
}

output_file = 'era5_data.nc'

try:
    print("downloading ERA5 data from CDS...")
    client = cdsapi.Client()
    client.retrieve(dataset, request, output_file)
    
    # Check if file was successfully created
    if not os.path.exists(output_file):
        print(f"ERROR: Download failed - file '{output_file}' was not created!")
        sys.exit(1)
    
    file_size = os.path.getsize(output_file)
    print(f"SUCCESS: Downloaded {output_file} ({file_size} bytes)")
    
except Exception as e:
    print(f"ERROR: Failed to download ERA5 data: {e}")
    print("Make sure you have a valid CDS API key configured.")
    sys.exit(1)