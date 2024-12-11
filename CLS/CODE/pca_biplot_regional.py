import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.colors import hsv_to_rgb
from sklearn.decomposition import PCA
import xarray as xr
import numpy as np
import sys

def read_loading_matrix(file_path):
    """Lire une matrice de chargement à partir d'un chemin de fichier."""
    return pd.read_csv(file_path, index_col=0)

def generate_distinct_colors(n):
    """Générer n couleurs distinctes."""
    hsv_colors = [(i / n, 0.7, 0.9) for i in range(n)]  # Saturation et Value fixes, Hue varie
    rgb_colors = [hsv_to_rgb(color) for color in hsv_colors]
    return rgb_colors

def superposed_biplot_2d(loadings_list, colors, labels, feature_names, biplot_path=None):
    plt.figure(figsize=(10, 7))

    # Générer une couleur distincte pour chaque variable
    variable_colors = generate_distinct_colors(len(feature_names))
    
    # Définir un ensemble de symboles pour les zones
    markers = ['o', 's', '^', 'D', '*', 'x', '+', 'v', '>']
    
    # S'assurer que nous avons assez de couleurs pour toutes les variables
    if len(feature_names) > len(variable_colors):
        print("Pas assez de couleurs définis pour toutes les variables.")
        return
    # S'assurer que nous avons assez de symboles pour toutes les zones
    if len(labels) > len(markers):
        print("Pas assez de symboles définis pour toutes les zones.")
        return
    
    legend_handles_zones = []  # Liste pour stocker les proxies de légende pour les zones
    legend_handles_variables = []  # Liste pour stocker les proxies de légende pour les variables
    
    # Dessiner les points pour la zone globale avec un symbole spécifique pour chaque variable
    for i, feature_name in enumerate(feature_names):
        plt.scatter(loadings_list[0].loc[feature_name, 'PC1'], loadings_list[0].loc[feature_name, 'PC2'], 
                    marker=markers[0], color=variable_colors[i], s=50, label='Global' if i == 0 else '')
        if i == 0:
                legend_handles_zones.append(mlines.Line2D([], [], color='black', marker=markers[0], linestyle='None', label='Global'))

    # Dessiner les points pour chaque zone avec un symbole spécifique pour la zone
    for j, (loadings, color, label) in enumerate(zip(loadings_list[1:], colors, labels[1:]), start=1):
        for i, feature_name in enumerate(feature_names):
            plt.scatter(loadings.loc[feature_name, 'PC1'], loadings.loc[feature_name, 'PC2'],
                        marker=markers[j % len(markers)], color=variable_colors[i], alpha=0.8)
            # Ajouter un proxy pour la légende lors du premier passage seulement
            if i == 0:
                legend_handles_zones.append(mlines.Line2D([], [], color='black', marker=markers[j % len(markers)], linestyle='None', label=label))
    
    # Ajouter les noms des variables d'origine avec leur couleur
    for i, feature_name in enumerate(feature_names):
        #plt.annotate(feature_name, xy=(loadings_list[0].iloc[i, 0], loadings_list[0].iloc[i, 1]),
                     #xytext=(0,10), textcoords="offset points", ha='center', va='center', 
                     #fontsize=9, color=variable_colors[i])
        legend_handles_variables.append(mlines.Line2D([], [], color=variable_colors[i], marker='o', linestyle='None', alpha=0.8, label=feature_name))

    
    plt.axhline(0, color='black', alpha=0.3, linewidth=1.5)
    plt.axvline(0, color='black', alpha=0.3, linewidth=1.5)

    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("2D Biplot of PCA")
    plt.grid(True)
    plt.axis('equal')
    #plt.legend(handles=legend_handles, loc='lower left') 
    first_legend = plt.legend(handles=legend_handles_zones, loc='upper right', title="Area", fontsize='small')
    plt.gca().add_artist(first_legend)
    plt.legend(handles=legend_handles_variables, loc='lower left', title="Variable", fontsize='small')
    
    
    if biplot_path:
        plt.savefig(biplot_path)
    plt.show()

    

    
def calculate_and_save_loadings(ds, filename):
    """
    Calcule et sauvegarde la matrice de chargement pour un dataset donné.
    """
    # Conversion en DataFrame Pandas, en excluant les colonnes non numériques et lessorties
    ds = ds.drop_vars(["LONGITUDE", "LATITUDE"])
    df = ds.to_dataframe().reset_index()
    df = df.drop(columns=['time'])
    df = df.drop(columns=["SSH_anomaly_corrected_ssb", "SSH_anomaly_uncorrected_ssb"], axis=1)
    
    # Application de l'ACP
    pca = PCA(n_components=2)  # Modifier selon le besoin
    pca.fit(df)
    
    # Création de la matrice de chargement
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
    loading_matrix = pd.DataFrame(loadings, columns=['PC1', 'PC2'], index=df.columns)
    
    # Sauvegarde de la matrice de chargement
    loading_matrix.to_csv(filename)
    
    return loading_matrix


def main(dataset_name):

    # Mappage des noms d'entrée aux indices numériques
    dataset_map = {"SAR": 1, "ERA5": 2, "LRM": 3}
    if dataset_name not in dataset_map:
        raise ValueError("Invalid dataset name. Please choose 'SAR', 'ERA5', or 'LRM'.")
    dataset_choice = dataset_map[dataset_name]

    # Zones à comparer, y compris le global ('None' pour global)
    zones = [None, 'NorthPacific', 'Equator', 'SouthPacific', 'NorthWestPacific', 'SouthEastPacific', 'IndianOcean', 'WideTropics']
    
    for zone in zones:
        # Chemin vers le fichier dataset
        file_path = f"dataset/dataset_{dataset_name}_2022_{zone + '_' if zone else ''}scaled.nc"
        ds = xr.open_dataset(file_path)
        print("Calcul de la matrice de chargement pour la zone :", zone if zone else 'Global')
        
        # Chemin pour sauvegarder la matrice de chargement
        loading_matrix_filename = f"results/loading_matrix_{dataset_name}{'_' + zone if zone else ''}.csv"
        
        # Calcul et sauvegarde de la matrice de chargement
        loading_matrix = calculate_and_save_loadings(ds, loading_matrix_filename)
        print("Loading matrix:\n", loading_matrix)
        
        print(f"Matrice de chargement pour {zone if zone else 'Global'} sauvegardée dans {loading_matrix_filename}.")


    # Chemins des fichiers de matrices de chargement
    file_paths = [f"results/loading_matrix_{dataset_name}{'_' + zone if zone else ''}.csv" for zone in zones]
    loadings_list = [read_loading_matrix(path) for path in file_paths]
    
    # Générer des couleurs
    colors = generate_distinct_colors(len(zones)-1)  # -1 car le global est toujours noir
    #labels = ['Global'] + [zone.capitalize() for zone in zones[1:]]  # Labels pour la légende
    labels = ['Global'] + [' '.join([word if index == 0 else word[0] + ''.join([' '+char if char.isupper() else char for char in word[1:]]) for index, word in enumerate(zone.split())]) for zone in zones[1:]]
    feature_names = loadings_list[0].index.tolist()  # Noms des variables depuis la matrice globale
    
    superposed_biplot_2d(loadings_list, colors, labels, feature_names, biplot_path=f"results/biplot_2d_{dataset_name}_regional.png")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dataset_name = sys.argv[1]
        main(dataset_name)
    else:
        print("Usage: python script.py <dataset_name>")
        print("Example: python script.py SAR")