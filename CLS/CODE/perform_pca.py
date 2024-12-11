import sys
import pandas as pd
from pca_analysis import PCAAnalysis
import xarray as xr

def main(dataset_name, nom_zone=None):
    # Mappage des noms d'entrée aux indices numériques
    dataset_map = {"SAR": 1, "ERA5": 2, "LRM": 3}
    if dataset_name not in dataset_map:
        raise ValueError("Invalid dataset name. Please choose 'SAR', 'ERA5', or 'LRM'.")
    dataset_choice = dataset_map[dataset_name]

    # Chemin de base pour les fichiers de dataset
    print(f"Recherche du fichier dataset {dataset_name} {nom_zone if nom_zone else ''}")
    base_path = f"dataset/dataset_{dataset_name}_2022_{nom_zone + '_' if nom_zone else ''}scaled.nc"

    # Lecture du dataset
    ds = xr.open_dataset(base_path)
    ds = ds.drop_vars(["LONGITUDE", "LATITUDE"])
    df = ds.to_dataframe().reset_index()
    df = df.drop(columns=['time'])

    # Initialisation de l'analyse PCA
    print('Début analyse')
    pca_analysis = PCAAnalysis(df, exclude_columns=["SSH_anomaly_corrected_ssb", "SSH_anomaly_uncorrected_ssb"])

    # Affichage de la matrice de corrélation
    corr_matrix = pca_analysis.plot_correlation_matrix(plot_path=f"results/corr_matrix_{dataset_name}{'_' + nom_zone if nom_zone else ''}.png")
    print("Correlation Matrix :\n", corr_matrix)

    # Détermination du nombre de composantes et application de l'ACP
    num_components = pca_analysis.choose_number_of_components(threshold=0.90, plot_path=f"results/variance_explained_{dataset_name}{'_' + nom_zone if nom_zone else ''}.png")
    transformed_data, loading_matrix = pca_analysis.apply_pca(n_components=num_components, save_path_csv=f"results/loading_matrix_{dataset_name}{'_' + nom_zone if nom_zone else ''}.csv", save_path_nc=f"results/principal_components_{dataset_name}{'_' + nom_zone if nom_zone else ''}.nc")
    print("Loading Matrix:\n", loading_matrix)

    # Génération et sauvegarde du biplot
    exclude_columns = ["SSH_anomaly_corrected_ssb", "SSH_anomaly_uncorrected_ssb"]
    pca_analysis.biplot_2d(transformed_data, loading_matrix, feature_names=df.drop(columns=exclude_columns).columns, biplot_path=f"results/biplot_2d_{dataset_name}{'_' + nom_zone if nom_zone else ''}.png")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dataset_name = sys.argv[1]
        nom_zone = sys.argv[2] if len(sys.argv) > 2 else None
        main(dataset_name, nom_zone)
    else:
        print("Usage: python script.py <dataset_name> <nom_zone>")
        print("Example: python script.py SAR WideTropics")
