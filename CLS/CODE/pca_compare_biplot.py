import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb

def read_loading_matrices(file_paths):
    """Lire les matrices de chargement à partir d'une liste de chemins de fichiers."""
    return [pd.read_csv(path, index_col=0) for path in file_paths]

def generate_distinct_colors(n):
    """Générer n couleurs distinctes."""
    hsv_colors = [(i / n, 0.7, 0.9) for i in range(n)]  # Saturation et Value fixes, Hue varie
    rgb_colors = [hsv_to_rgb(color) for color in hsv_colors]
    return rgb_colors

def superposed_biplot_2d(pca_results, loadings_list, colors, dataset_labels, feature_names, biplot_path=None):
    """
    Dessine un biplot 2D superposé pour plusieurs résultats d'ACP, incluant une légende pour les datasets
    et affichant les noms des variables d'origine.
    """
    plt.figure(figsize=(10, 7))
    
    # Afficher les points pour chaque ensemble de résultats PCA
    for i, (pca_result, color, label) in enumerate(zip(pca_results, colors, dataset_labels)):
        plt.scatter(pca_result[:, 0], pca_result[:, 1], color=color, alpha=0.5, label=label)
    
    # Ajouter les noms des variables d'origine en utilisant plt.annotate
    for i, feature_name in enumerate(feature_names):
        plt.annotate(feature_name, xy=(loadings_list[0].iloc[i, 0], loadings_list[0].iloc[i, 1]), 
                     xytext=(0,10), textcoords="offset points", ha='center', va='center', fontsize=9)

    # Dessiner les lignes d'axes à zéro en gras
    plt.axhline(0, color='black', alpha=0.3, linewidth=2) 
    plt.axvline(0, color='black', alpha=0.3, linewidth=2)

    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("Overlaid 2D Biplot of PCA for different datasets")
    plt.grid(True)
    plt.axis('equal')
    plt.legend()

    if biplot_path:
        plt.savefig(biplot_path)
    plt.show()

def main(dataset_names):
    colors = generate_distinct_colors(len(dataset_names))
    dataset_labels = [f"Dataset {n}" for n in dataset_names]
    feature_names = ['Orbital_velocity_std', 'Stokes_Drifts_prof_on_Satellite_Direction', 'Mean_Wave_Period', 'Wind_Speed_Alti', 'SWH_Alti']
    file_paths = [f"results/loading_matrix_{n}.csv" for n in dataset_names]
    loadings_list = read_loading_matrices(file_paths)
    feature_names = loadings_list[0].index.tolist()
    pca_results = [loading.values[:, :2] for loading in loadings_list]
    biplot_path = f"results/biplot_comparison_{'_'.join(map(str, dataset_names))}.png"
    superposed_biplot_2d(pca_results, loadings_list, colors, dataset_labels, feature_names, biplot_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dataset_names = list(map(str, sys.argv[1:]))
        main(dataset_names)
    else:
        print("Usage: python script.py <dataset_name_1> <dataset_name_2> ...")
        print("Example: python script.py SAR ERA5 LRM")