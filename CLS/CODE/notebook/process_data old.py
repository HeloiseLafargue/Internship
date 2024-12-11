import os
import sys
import xarray as xr
import pandas as pd
from casys import CasysPlot, DateHandler, Field, NadirData, PlotParams
from casys.readers import CLSTableReader, MultiReader
from sklearn.preprocessing import StandardScaler

def main(dataset_name):
    # Mappage des noms d'entrée aux indices numériques
    dataset_map = {"SAR": 1, "ERA5": 2, "LRM": 3}
    if dataset_name not in dataset_map:
        raise ValueError("Invalid dataset name. Please choose 'SAR', 'ERA5', or 'LRM'.")
    dataset_choice = dataset_map[dataset_name]

    # Variable d'environnement contenant les tables
    ges_table_dir = "/data/SSB_ETU/S6JTEX/DSC"
    os.environ["GES_TABLE_DIR"] = ges_table_dir
    os.environ["OCE_DATA"] = "/data/SUPPORT/DONNEES/"

    # Tables
    table_lr = CLSTableReader(name="TABLE_C_S6A_LR_B")  # Table S6 LR​
    table_lr_enrichie = CLSTableReader(name="TABLE_C_S6A_LR_B_S6JTEX")  # Table LR enrichie
    table_hr = CLSTableReader(name="TABLE_C_S6A_HR_B")  # Table S6 HR
    table_hr_enrichie = CLSTableReader(name="TABLE_C_S6A_HR_B_S6JTEX")  # Table HR enrichie

    # Nom de l'orbit file
    ORF = "C_S6A_LR_ORF"

    # Période
    start = DateHandler.from_orf(orf=ORF, cycle_nb=42, pass_nb=73, pos="first")
    end = DateHandler.from_orf(orf=ORF, cycle_nb=79, pass_nb=23, pos="last")

    print("Period start :", start)
    print("Period end :", end)

    # Sélection du dataset
    if int(dataset_choice) == 1:
        fields = [
            Field(name="SWH_Alti", source="HR_SWH.ALTI"),
            Field(name="Wind_Speed_Alti", source="HR_WIND_SPEED.ALTI")
        ]
    elif int(dataset_choice) == 2:
        fields = [
            Field(name="SWH_Model", source="LR_SWH_ERA5"),
            Field(name="Wind_Speed_Model", source="LR_WIND_SPEED_ERA5")
        ]
    elif int(dataset_choice) == 3:
        fields = [
            Field(name="SWH_Alti", source="LR_SWH.ALTI"),
            Field(name="Wind_Speed_Alti", source="LR_WIND_SPEED.ALTI")
        ]
    else:
        raise ValueError("Invalid dataset choice. Please choose 1, 2, or 3.")

    fields += [
        Field(name="Mean_Wave_Period", source="LR_T02_ERA5"),
        Field(name="Stokes_Drifts_prof_on_Satellite_Direction", source="LR_VELOCITY_STOKES_DRIFT_PROJ_ERA5"),
        Field(name="Orbital_velocity_std", source="LR_ORBITAL_VELOCITY_STD"),
        Field(name="SSH_anomaly_corrected_ssb", source="HR_SEA_SURFACE_HEIGHT_ANOMALY.ALTI"),
        Field(name="SSH_anomaly_uncorrected_ssb", source="HR_SEA_SURFACE_HEIGHT_ANOMALY_UNCORR_SSB.ALTI")
    ]

    # Création de l'objet NadirData
    ad = NadirData(
        source=MultiReader(
            readers=[table_lr_enrichie, table_hr_enrichie],
            markers=["LR_", "HR_"],
            date_start=start,
            date_end=end,
            orf=ORF,
            select_clip="LR_FLAG_VAL.ALTI:==0",
            time="time",
            longitude="LONGITUDE",
            latitude="LATITUDE",
        )
    )

    # Ajout des champs au NadirData
    for field in fields:
        ad.add_raw_data(name=field.name, field=field)

    ad.compute()

    ds = ad.data.dropna(dim="time")

    # Enregistrement des données initiales
    filename_base = f"dataset{dataset_choice}_2022"
    ds.to_netcdf(f"dataset/{filename_base}.nc")

    # Conversion en DataFrame et réinitialisation de l'index
    df = ds.to_dataframe().reset_index()
    print("Statistiques du dataset:\n")
    print(df.describe())

    # Identification des colonnes numériques pour la standardisation
    # Exclut les colonnes de type object, bool, datetime, etc.
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.difference(['LONGITUDE', 'LATITUDE'])
    
    # Standardisation des données numériques
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    print("Statistiques du dataset standardisé:\n")
    print(df.describe())

    # Reconversion du DataFrame standardisé en xarray.Dataset
    ds_scaled = xr.Dataset.from_dataframe(df.set_index(['time']))
    
    # Enregistrement des données standardisées au format NetCDF
    ds_scaled.to_netcdf(f"dataset/{filename_base}_scaled.nc")
    
    print(f"Dataset {dataset_choice} processed and saved.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dataset_choice = sys.argv[1]
        main(dataset_choice)
    else:
        print("Usage: python script.py <dataset_number>")
        print("Example: python script.py 1")