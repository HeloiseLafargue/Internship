import sys
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

def main():
    # Chemins des fichiers
    files = [
        "/data/SSB_ETU/HLAFARGUE/S6JTEX/dataset/dataset_SAR_2022.nc",
        "/data/SSB_ETU/HLAFARGUE/S6JTEX/dataset/dataset_ERA5_2022.nc",
        "/data/SSB_ETU/HLAFARGUE/S6JTEX/dataset/dataset_LRM_2022.nc"
    ]

    # Noms des datasets pour la légende
    dataset_names = ["SAR", "ERA-5", "LRM"]
    colors = ['c', 'm', 'y'] 

    # Variables à exclure
    exclude_vars = ['LONGITUDE', 'LATITUDE', 'SSH_anomaly_corrected_ssb', 'SSH_anomaly_uncorrected_ssb']

    # Initialisation de la figure
    plt.figure(figsize=(14, 8))

    # Mapping des noms génériques pour les variables groupées
    variable_mapping = {
        'SWH_Alti': 'SWH',
        'SWH_Model': 'SWH',
        'Wind_Speed_Alti': 'Wind Speed',
        'Wind_Speed_Model': 'Wind Speed'
    }

    # Ensemble pour collecter les variables pour les x-ticks
    x_tick_vars = set()

    # Dictionnaire pour suivre les indices de graphiques pour les variables groupées
    var_indices = {}

    # Pour chaque fichier
    for i, file_path in enumerate(files):
        
        # Lire le fichier NetCDF
        data = xr.open_dataset(file_path)

        # Filtrer les variables
        filtered_data = data.drop_vars(exclude_vars, errors='ignore')
        df = filtered_data.to_dataframe().reset_index()
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.difference(exclude_vars)

        print(f'\nStatistics on set {dataset_names[i]}')

        # Mise à jour de l'ensemble des variables
        for col in numeric_cols:
            generic_var_name = variable_mapping.get(col, col)
            if generic_var_name not in var_indices:
                var_indices[generic_var_name] = len(var_indices)
            x_tick_vars.add(generic_var_name)

            mean_val = df[col].mean()
            min_val = df[col].min()
            max_val = df[col].max()
            std_val = df[col].std()

            print('Variable:', generic_var_name)
            print('Mean: ', mean_val, ', min: ', min_val, ', max: ', max_val, ', std: ', std_val)

            # Ajouter les statistiques au graphique
            plt.errorbar(x=var_indices[generic_var_name] + i*0.2, y=mean_val, yerr=[[mean_val - min_val], [max_val - mean_val]],
                         fmt='o', capsize=5, elinewidth=2, label=f'{dataset_names[i]}' if col == numeric_cols[0] else "", color=colors[i])
            plt.text(var_indices[generic_var_name] + i*0.2, mean_val, f'±{std_val:.2f}', ha='center', va='bottom', color='black')

    # Configuration finale de la figure
    plt.xticks(range(len(var_indices)), [var[:16] for var in sorted(var_indices.keys())])  # Limitation à 15 caractères
    plt.ylabel('Value')
    plt.title('Variable Statistics Across Datasets')
    plt.legend(title='Dataset')
    plt.grid(True)

    # Sauvegarder la figure avant d'afficher
    plot_path = 'results/statistics.png'
    plt.savefig(plot_path)
    plt.show()

    # Fermer les fichiers pour libérer des ressources
    for file in files:
        data.close()

if __name__ == "__main__":
    main()
