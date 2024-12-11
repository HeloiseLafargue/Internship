import matplotlib.colors
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import sys

def main(dataset_choice):

    plot_pca_components_1d_histogram(dataset_choice)
    plot_pca_components_2d_histogram(dataset_choice)

def display_stats(data, label):
    """
    Affiche les statistiques de base d'un ensemble de données.
    """
    print(f"{label} stats:")
    print(f"Min: {np.min(data)}")
    print(f"Max: {np.max(data)}")
    print(f"Mean: {np.mean(data)}")
    print(f"Std: {np.std(data)}")

def plot_pca_components_1d_histogram(dataset_name):
    """
    Fonction pour tracer les histogrammes superposés des deux premières composantes principales.

    Parameters:
    - dataset_name: str, nom du dataset pour choisir le fichier NetCDF contenant les composantes principales.
    """
    # Chargement du dataset xarray
    base_path = f"results/principal_components_{dataset_name}.nc"
    plot_path = f"results/hist1D_PC1_PC2_{dataset_name}.png"
    ds = xr.open_dataset(base_path)

    # Extraction des données pour chaque variable (composante principale)
    data_pc1 = ds['PC1'].values.flatten()  # Flatten pour convertir en 1D si nécessaire
    data_pc2 = ds['PC2'].values.flatten()

    # Afficher les statistiques pour PC1 et PC2
    display_stats(data_pc1, "PC1")
    display_stats(data_pc2, "PC2")

    min_bin = min(data_pc1.min(), data_pc2.min())
    max_bin = max(data_pc1.max(), data_pc2.max())
    bins = np.arange(min_bin, max_bin + 0.25, 0.25)

    # Création de la figure et des axes pour les histogrammes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Tracé de l'histogramme pour PC1
    ax.hist(data_pc1, bins=bins, color='blue', alpha=0.5, label='PC1')

    # Tracé de l'histogramme pour PC2
    ax.hist(data_pc2, bins=bins, color='red', alpha=0.5, label='PC2')

    # Ajout des titres et des labels
    ax.set_title('1D histogram of PC1 and PC2')
    ax.set_xlabel('Values')
    ax.set_ylabel('Frequence')

    # Ajout d'une légende pour distinguer les composantes principales
    ax.legend()

    # Affichage et sauvegarde de la figure
    plt.savefig(plot_path)
    plt.show()


def plot_pca_components_2d_histogram(dataset_name):
    """
    Fonction pour tracer un histogramme 2D des deux premières composantes principales
    avec des boîtes de 0.5x0.5 dans l'espace formé par PC1 et PC2.

    Parameters:
    - dataset_name: str, nom du dataset pour choisir le fichier NetCDF contenant les composantes principales.
    """
    # Chargement du dataset xarray
    base_path = f"results/principal_components_{dataset_name}.nc"
    plot_path = f"results/hist2D_PC1_PC2_{dataset_name}.png"
    ds = xr.open_dataset(base_path)

    # Extraction des données pour chaque composante principale
    data_pc1 = ds['PC1'].values.flatten()
    data_pc2 = ds['PC2'].values.flatten()

    # Création de la figure et de l'axe pour l'histogramme 2D
    fig, ax = plt.subplots(figsize=(12,5))

    # Tracé de l'histogramme 2D
    # Utilisation de bins=np.arange(start, stop, step) pour créer des intervalles de 0.5
    x_edges = np.arange(data_pc1.min(), data_pc1.max() + 0.5, 0.5)
    y_edges = np.arange(data_pc2.min(), data_pc2.max() + 0.5, 0.5)

    # Tracer l'histogramme 2D
    hist, xedges, yedges, image = ax.hist2d(data_pc1, data_pc2, bins=[x_edges, y_edges], cmap='viridis', norm=matplotlib.colors.LogNorm())

    # Appliquer 10*log10(count) aux valeurs de l'histogramme, en évitant log10(0) par ajout de 1 à count
    hist_log_transformed = 10 * np.log10(hist + 1)
    
    # Utiliser les valeurs transformées pour la coloration de l'histogramme 2D
    pcm = ax.pcolormesh(xedges, yedges, hist_log_transformed.T, norm=matplotlib.colors.Normalize(), cmap='viridis')
    
    # Ajouter une barre de couleur reflétant 10*log10(count)
    cbar = fig.colorbar(pcm, ax=ax, label='10*log10(count)')

    # Niveaux pour les contours en termes de log10(count)
    levels = [1, 2, 3, 4]  # Correspond à 10^1, 10^2, 10^3, 10^4 en échelle linéaire

    # Tracer les contours
    X, Y = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25)  # Centre des bins
    CS = ax.contour(X, Y, np.log10(hist.transpose() + 1), levels=levels, colors='white')

    ax.clabel(CS, inline=True, fontsize=10, fmt='%1.0f')  # Formatter les labels de contour pour afficher la puissance de 10

    # Ajout des titres et des labels
    ax.set_title('2D histogram of PC1 vs PC2')
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')


    # Affichage et sauvegarde de la figure
    plt.savefig(plot_path)
    plt.show()



if __name__ == "__main__":
    if len(sys.argv) > 1:
        dataset_name = sys.argv[1]
        main(dataset_name)
    else:
        print("Usage: python script.py <dataset_name>")
        print("Example: python script.py SAR")
