import sys
import xarray as xr
import pandas as pd
from sklearn.preprocessing import StandardScaler

def extract_zone_from_nc(dataset_choice, nom_zone, lat1, lat2, lon1, lon2, lon3=None, lon4=None):
    """
    Filtre par zone géographique les variables au préalable standardisées (sauf LONGITUDE et LATITUDE).
    """
    # Récupération des données
    file_path = f"dataset/dataset{dataset_choice}_2022_scaled.nc"
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
    output_file_base = f"{nom_zone}_dataset{dataset_choice}_2022"
    ds_filtered.to_netcdf(f"dataset/{output_file_base}_scaled.nc")

    print(f"Extraction terminée. Les données standardisées et filtrées sont sauvegardées dans '{output_file_base}_scaled.nc'.")

if __name__ == "__main__":
    if len(sys.argv) > 6:
        dataset_choice = sys.argv[1]
        nom_zone = sys.argv[2]
        lat1 = float(sys.argv[3])
        lat2 = float(sys.argv[4])
        lon1 = float(sys.argv[5])
        lon2 = float(sys.argv[6])
        lon3 = float(sys.argv[7]) if len(sys.argv) > 7 else None
        lon4 = float(sys.argv[8]) if len(sys.argv) > 8 else None
        
        extract_zone_from_nc(dataset_choice, nom_zone, lat1, lat2, lon1, lon2, lon3, lon4)
    else:
        print("Usage: python script.py dataset_choice nom_zone lat1 lat2 lon1 lon2 [lon3 lon4]")
        print("Exemple: python script.py 1 PacifiqueNord 0 -60 -180 -100 120 180")
