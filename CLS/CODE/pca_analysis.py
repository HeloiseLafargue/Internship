import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import xarray as xr
import seaborn as sns 
import textwrap

class PCAAnalysis:
    def __init__(self, data, exclude_columns=None):
        if exclude_columns is not None:
            self.data = data.drop(exclude_columns, axis=1)
        else:
            self.data = data

    def plot_correlation_matrix(self, plot_path=None):
        """Génère et affiche la matrice de corrélation entre les variables du dataset."""
        corr_matrix = self.data.corr()
        plt.figure(figsize=(12, 10))
        xticklabels = [textwrap.fill(label, 16) for label in self.data.columns]
        yticklabels = [textwrap.fill(label, 16) for label in self.data.columns]
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True, 
                    xticklabels=xticklabels, yticklabels=yticklabels)
        plt.title("Correlation Matrix")
        plt.xticks(rotation=30)
        plt.yticks(rotation=0)
        if plot_path:
            plt.savefig(plot_path)
        plt.show()
        return corr_matrix

    def choose_number_of_components(self, threshold=0.90, plot_path=None):
        pca = PCA().fit(self.data)
        cumulative_variance_ratio = np.cumsum(pca.explained_variance_ratio_)
        num_components_threshold = np.argmax(cumulative_variance_ratio >= threshold) + 1 # +1 pour obtenir le nombre exact de composantes
        print("Nombre de composantes pour atteindre ou dépasser le seuil de variance expliquée de", threshold, ":", num_components_threshold)

        # Affichage de la variance expliquée par exactement 2 composantes
        if len(pca.explained_variance_ratio_) >= 2:
            variance_two_components = np.sum(pca.explained_variance_ratio_[:2])
            print("Variance expliquée avec 2 composantes:", variance_two_components)
            variance_two_components = np.sum(pca.explained_variance_ratio_[:3])
            print("Variance expliquée avec 3 composantes:", variance_two_components)
        else:
            print("Moins de 2 composantes disponibles.")

        plt.figure(figsize=(10, 5))
        plt.plot(range(1, len(cumulative_variance_ratio)+1), cumulative_variance_ratio, marker='o')
        plt.xlabel("Number of Principal Components")
        plt.ylabel("Cumulative Explained Variance")
        plt.title("Elbow Method for PCA")
        plt.axhline(y=threshold, color='r', linestyle='--')
        plt.axvline(x=num_components_threshold, color='r', linestyle='--')

        if plot_path:
            plt.savefig(plot_path)
        plt.show()

        return num_components_threshold

    def apply_pca(self, n_components, save_path_csv, save_path_nc):
        pca = PCA(n_components=n_components)
        transformed_data = pca.fit_transform(self.data)
        # Calcul des loadings
        loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
        # Création de la matrice de chargement
        loading_matrix = pd.DataFrame(loadings, columns=[f"PC{i+1}" for i in range(n_components)], index=self.data.columns)
        # Sauvegarde de la matrice de chargement en CSV
        loading_matrix.to_csv(save_path_csv)

        # Avec 2 composantes
        # Convertir les données transformées en DataFrame
        pca = PCA(n_components=2)
        transformed_data_2d = pca.fit_transform(self.data)
        transformed_df = pd.DataFrame(transformed_data_2d, columns=[f"PC{i+1}" for i in range(2)])
        # Conversion du DataFrame pandas en xarray Dataset
        ds = xr.Dataset.from_dataframe(transformed_df)
        # Sauvegarde du Dataset xarray en fichier NetCDF
        ds.to_netcdf(save_path_nc)
        return transformed_data, loading_matrix

    def biplot_2d(self, pca_result, loadings, feature_names, biplot_path=None):
        plt.figure(figsize=(10, 7))
        for i, feature in enumerate(feature_names):
            plt.arrow(0, 0, loadings.iloc[i, 0], loadings.iloc[i, 1], color='red', alpha=0.5)
            plt.text(loadings.iloc[i, 0]*1.15, loadings.iloc[i, 1]*1.15, feature, color='green', ha='center', va='center')

        plt.xlabel("PC1")
        plt.ylabel("PC2")
        plt.title("2D PCA Biplot")
        plt.grid(True)
        plt.axis('equal')

        if biplot_path:
            plt.savefig(biplot_path)
        plt.show()
