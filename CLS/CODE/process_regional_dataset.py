import subprocess
import sys
import xarray as xr
import pandas as pd
from sklearn.preprocessing import StandardScaler

def extract_zone_from_nc(dataset_name, nom_zone, lat1, lat2, lon1, lon2, lon3=None, lon4=None):
    """
    Filtre par zone géographique les variables au préalable standardisées (sauf LONGITUDE et LATITUDE).
    """
    # Récupération des données
    file_path = f"dataset/dataset_{dataset_name}_2022_scaled.nc"
    ds = xr.open_dataset(file_path)

    # Application du filtre géographique en utilisant `where` de xarray
    condition_lat = (ds['LATITUDE'] >= lat1) & (ds['LATITUDE'] <= lat2)
    if lon3 and lon4:
        # Gérer une plage de longitude discontinue
        condition_lon = ((ds['LONGITUDE'] >= lon1) & (ds['LONGITUDE'] <= lon2)) | ((ds['LONGITUDE'] >= lon3) & (ds['LONGITUDE'] <= lon4))
    else:
        condition_lon = (ds['LONGITUDE'] >= lon1) & (ds['LONGITUDE'] <= lon2)
    
    ds_filtered = ds.where(condition_lat & condition_lon, drop=True)

    # Enregistrement des résultats
    output_file_base = f"dataset_{dataset_name}_2022_{nom_zone}"
    ds_filtered.to_netcdf(f"dataset/{output_file_base}_scaled.nc")

    print(f"Extraction terminée. Les données standardisées et filtrées sont sauvegardées dans '{output_file_base}_scaled.nc'.")

def process_zones(dataset_name):
    zones = ['NorthPacific', 'Equator', 'SouthPacific', 'NorthWestPacific', 'SouthEastPacific', 'IndianOcean', 'WideTropics']
    latitudes = [[0, 60], [-20, 20], [-60, 0], [20, 70], [-60, -10], [-20, 30], [-30,30]]
    longitudes = [
        [[-180, -100], [120, 180]],
        [[-180, -20], [140, 180]],
        [[-180, -80], [140, 180]],
        [120, 180],
        [-120, -70],
        [40, 100],
        [-162, 20]
    ]

    for zone, lat, lon in zip(zones, latitudes, longitudes):
        if isinstance(lon[0], list):
            extract_zone_from_nc(dataset_name, zone, lat[0], lat[1], lon[0][0], lon[0][1], lon[1][0], lon[1][1])
        else:
            extract_zone_from_nc(dataset_name, zone, lat[0], lat[1], lon[0], lon[1])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dataset_name = sys.argv[1]
        process_zones(dataset_name)
    else:
        print("Usage: python script.py <dataset_name>")
        print("Example: python script.py SAR")
