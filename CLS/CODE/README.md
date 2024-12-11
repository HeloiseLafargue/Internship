# README

## Overview
This README provides details on two Python scripts designed for the analysis of satellite oceanographic data. Each script is tailored for specific tasks in the data processing pipeline and principal component analysis pipeline.

## Scripts Description

### 1. `process_data.py`

**Description:**  
`process_data.py` processes satellite oceanographic data using specific tools and libraries. It handles different dataset types identified as "SAR", "ERA5", or "LRM" through command line arguments.

**Key Features and Workflow:**
1. **Environment Setup:** Sets necessary environmental variables (`GES_TABLE_DIR` and `OCE_DATA`) for accessing data tables from the file system.
2. **Data Readers Initialization:** Utilizes `CLSTableReader` and `MultiReader` from the `casys` library to manage and parse tables for various dataset resolutions (LR and HR).
3. **Time Period and Data Field Selection:** Uses `DateHandler` to define the processing period and selects relevant data fields such as sea wave height, wind speed, and sea surface height anomalies.
4. **Data Processing:** Creates an instance of `NadirData`, populates it with selected data fields, and performs computations. Data selection criteria include geographic and variability constraints.
5. **Data Standardization and Saving:** Standardizes data using `StandardScaler` and saves both raw and processed data in NetCDF format.
6. **Modularity and Error Handling:** Structured with distinct functions for each processing step to enhance readability and maintenance, with robust error handling for dataset naming.

**Usage Instructions:**
Run from the command line with a dataset name as an argument. Example: `python process_data.py SAR`

### 2. `visualize_statistics.py`

**Description:**  
`visualize_statistics.py` visualizes statistical properties of various satellite datasets using `xarray` for data handling and `matplotlib` for plotting, facilitating comparative analysis across different datasets.

**Key Features and Workflow:**
1. **Data Loading:** Opens predefined NetCDF files containing processed data for datasets such as "SAR", "ERA-5", and "LRM".
2. **Variable Selection and Mapping:** Excludes non-essential variables and maps significant variables like wave heights and wind speeds to generic names for consistency.
3. **Statistical Computation:** Calculates mean, minimum, maximum, and standard deviation for each variable across datasets, helping to evaluate data dispersion and central tendency.
4. **Error Bar Plotting:** Visualizes data using error bars that display ranges and standard deviations, with color coding and labels for each dataset.
5. **Figure Configuration:** Adjusts plot settings including labels, title, grid, and a legend to improve readability and aesthetics.
6. **Resource Management and Output:** Saves the plot to a file and ensures all data files are closed post-visualization to free up resources.

**Usage Instructions:**
Execute directly from the command line without any arguments. Example: `python visualize_statistics.py`

### 3. `perform_pca.py`

**Description:**  
`perform_pca.py` executes a comprehensive PCA on specified oceanographic datasets to identify principal components that capture the most variance, providing insights into underlying patterns in the data. The script can handle different datasets and optionally focuses on specific geographic zones.

**Key Features and Workflow:**
1. **Dataset Mapping and Loading:** Maps textual dataset identifiers to numeric indices and dynamically constructs file paths to load specific or regional datasets using `xarray`.
2. **Data Preprocessing:** Removes non-analytical variables like geographical coordinates and converts the data into a `pandas` DataFrame, dropping unnecessary time indices for PCA.
3. **PCA Initialization and Execution:** Initializes PCA analysis by excluding specific variables, computes the correlation matrix, and identifies the number of principal components that explain a predefined variance threshold.
4. **Results Visualization:** Outputs several plots:
   - Correlation matrix of variables to understand interdependencies.
   - Scree plot indicating variance explained by each principal component.
   - A 2D biplot showing the projection of both the samples and variables in the space defined by the first two principal components.
5. **Data Export:** Saves the loading matrix and principal components to CSV and NetCDF files respectively, allowing for further analysis or archiving.

**Usage Instructions:**
Run from the command line, specifying the dataset and optionally a specific geographic zone. The script expects the dataset name and the zone name (if applicable) as command line arguments. Example: `python perform_pca.py SAR ` or `python perform_pca.py ERA5 WideTropics`

### 4. `pca_analysis.py`

**Description:**  
`pca_analysis.py` is a utility module that performs PCA (used in `perform_pca.py`) on given datasets to uncover underlying patterns, reduce dimensionality, and visualize the relationships between variables. This script is typically used as an import in other scripts to facilitate advanced data analysis tasks.

**Key Features and Workflow:**
1. **Initialization and Data Preparation:** Initializes with a dataset, optionally excluding specified columns. This step prepares the data for subsequent PCA analysis.
2. **Correlation Matrix Visualization:** Generates and displays a heatmap of the correlation matrix, which helps in understanding the interdependencies among the variables.
3. **Principal Component Determination:** Utilizes the cumulative variance ratio to determine the number of components needed to explain a predefined threshold of total variance, supporting decisions on dimensionality reduction.
4. **PCA Execution and Loading Matrix Creation:** Applies PCA to the data to reduce dimensions and calculates the loading matrix, which indicates how much each variable contributes to the principal components.
5. **PCA Transformation and Saving:** Transforms the data into principal component space and saves both the loading matrix and the transformed data in CSV and NetCDF formats, respectively.
6. **Biplot Generation:** Provides a 2D visualization of the first two principal components with vectors representing the original variables, which can be very insightful for visualizing how variables contribute to the components.

**Usage Instructions:**
This script is not meant to be run as a standalone script but is intended to be imported into other Python scripts or Jupyter notebooks where PCA-related tasks are required. Here is an example of how to use this module in another script:

```python
from pca_analysis import PCAAnalysis

# Assuming `data` is a Pandas DataFrame of your dataset
pca = PCAAnalysis(data, exclude_columns=['non_feature1', 'non_feature2'])
correlation_matrix = pca.plot_correlation_matrix("path_to_save_plot.png")
num_components = pca.choose_number_of_components(threshold=0.90, plot_path="path_to_save_variance_plot.png")
transformed_data, loading_matrix = pca.apply_pca(n_components=num_components, save_path_csv="path_to_loading_matrix.csv", save_path_nc="path_to_transformed_data.nc")
pca.biplot_2d(transformed_data, loading_matrix, data.columns, "path_to_save_biplot.png")
```

### 5. `pca_compare_biplot.py`

**Description:**  
`pca_compare_biplot.py` facilitates the visualization of Principal Component Analysis (PCA) loadings and scores for multiple datasets on a single biplot. The script is especially useful for comparative analysis, allowing researchers to visually assess relationships and differences between datasets in terms of their principal components.

**Key Features and Workflow:**
1. **Loading Data:** Reads PCA loading matrices from CSV files for multiple datasets. These matrices contain the coordinates of each variable in the principal component space.
2. **Color Coding:** Generates a distinct color for each dataset to help differentiate them in the visual output.
3. **Biplot Construction:** Constructs a 2D biplot where both the PCA scores (dataset projections) and PCA loadings (variable vectors) are plotted. This is done for multiple datasets simultaneously, with each dataset distinctly colored.
4. **Visualization Enhancements:**
   - Variable names are annotated directly on the plot for clear identification.
   - Zero lines for both axes are emphasized to aid interpretation.
   - The plot includes a legend identifying each dataset by name, grid lines for better visualization, and axes labeled as "PC1" and "PC2".
5. **Output and Display:** Optionally saves the biplot to a specified path and displays it interactively.

**Usage Instructions:**
Execute from the command line, specifying multiple dataset names as arguments. Example: `python pca_compare_biplot.py SAR ERA5 LRM`

### 6. `map_regions.py`

**Description:**  
`map_regions.py` is a Python script aimed at visualizing distinct geographic regions relevant to oceanographic research. The script uses cartographic projections to plot specified areas on a global map, highlighting these regions with distinct colors.

**Key Features and Workflow:**
1. **Data Definition:** Specifies the names, latitude ranges, and longitude ranges of various study zones such as the North Pacific, Equator, South Pacific, and others.
2. **Map Setup:** Creates a map using `cartopy`'s `PlateCarree` projection, which is commonly used for global maps due to its simplicity and effectiveness in displaying geographic data.
3. **Region Plotting:** Uses `Rectangle` patches to represent the geographic regions on the map. Handles both continuous and discontinuous longitude ranges, accommodating the wrap-around nature of the map.
4. **Color Coding:** Implements a function `generate_distinct_colors` to create a unique color for each region, enhancing the map’s readability and visual appeal.
5. **Plot Customization:** Configures the map with coastlines, borders, and a grid of longitude and latitude lines. Also, formats tick labels for clear geographic referencing.
6. **Output and Display:** Saves the visual output as a PNG file with high resolution and displays the plot interactively.

**Usage Instructions:**
Execute directly from the command line without any arguments. Example: `python map_regions.py`

### 7. `process_regional_dataset.py`

**Description:**  
`process_regional_dataset.py` automates the extraction and processing of regional datasets from a global standardized dataset. It utilizes geographic coordinates to filter data relevant to specified oceanographic regions, enhancing targeted analyses.

**Key Features and Workflow:**
1. **Data Extraction:** Filters data from a global dataset based on latitude and longitude ranges. It supports both continuous and discontinuous longitude ranges, accommodating global geographic complexities.
2. **Regional Dataset Creation:** Each region's data is saved as a separate NetCDF file, maintaining the standardized format. The script processes multiple predefined regions in sequence.
3. **Automated Processing:** Integrates the extraction logic within a loop that processes an array of geographic zones, enabling efficient handling of multiple regions in one execution.
4. **Output Management:** Saves each regional dataset with a naming convention that incorporates the region name and the dataset identifier, making it easy to identify and retrieve specific regional datasets.
5. **Flexible Region Definitions:** The script can easily be adapted to include additional regions or modify existing ones by adjusting the latitude and longitude parameters in the `process_zones` function.

**Usage Instructions:**
The script is executed from the command line, requiring the name of the dataset as an argument. It processes all predefined regions for the specified dataset automatically. Example: `python process_regional_dataset.py SAR`

### 8. `pca_biplot_regional.py`

**Description:**  
`pca_biplot_regional.py` performs PCA on satellite oceanographic data for specified global and regional datasets and generates a superposed 2D biplot. This biplot helps in understanding the variable contributions and differences across various regions.

**Key Features and Workflow:**
1. **Loading Matrix Calculation:** Processes each region's data to calculate PCA loading matrices, which are saved to CSV files. This includes global data as well as specific regions like the North Pacific, Equator, etc.
2. **Biplot Generation:** Constructs a 2D biplot displaying PCA loadings (variable vectors) for multiple regions simultaneously. The script uses distinct markers and colors to differentiate regions and variables, respectively.
3. **Visualization Enhancements:** Enhances plot readability by annotating variable names directly on the biplot, emphasizing zero lines for axes, and using a grid for better visual alignment.
4. **Legend Management:** Includes dual legends to differentiate between regions (area) and variables, helping in easy identification of plotted elements.
5. **Output Management:** Optionally saves the biplot to a specified path for future reference or presentations.

**Usage Instructions:**
The script is executed from the command line, requiring the name of the dataset as an argument. It processes predefined regions automatically and generates a biplot comparing these regions. Example:`python pca_biplot_regional.py SAR`

### 9. `histogrammes.py`

**Description:**  
`histogrammes.py` creates comprehensive visual representations of principal components through histograms. It visualizes the distribution of PC1 and PC2 in both one-dimensional and two-dimensional formats, highlighting their frequency and correlation.

**Key Features and Workflow:**
1. **Histogram Plotting:**
   - **1D Histograms:** Plots superposed histograms for the first and second principal components (PC1 and PC2), allowing for comparison of their distributions within the same figure.
   - **2D Histogram:** Visualizes the joint distribution of PC1 and PC2, using a 2D histogram with logarithmic color scaling to highlight areas of higher and lower density.
2. **Data Extraction and Handling:** Loads principal component data from a NetCDF file specified by the dataset name, extracting values for PC1 and PC2.
3. **Statistical Analysis:** Computes and displays basic statistics for each principal component, such as minimum, maximum, mean, and standard deviation.
4. **Visualization Enhancements:** 
   - **Color Mapping:** Utilizes a logarithmic normalization for the 2D histogram to enhance the visibility of ranges with varying densities.
   - **Contour Plotting:** Adds contour lines to the 2D histogram to outline levels of data density, providing clear demarcations of major distribution thresholds.
5. **Interactive and Save Options:** Both types of histograms are displayed interactively and can be saved as PNG files for documentation or further analysis.

**Usage Instructions:**
The script is run from the command line, requiring the name of the dataset as an argument. It processes the specified dataset and generates both types of histograms automatically. Example: `python histogrammes.py SAR`

### 10. `kernel_method_analysis/crossover_octant.ipynb`

notebook pour faire l'évaluation des résultats aux points de croisement, par la différence de variances de delta_ssh

### 11. `kernel_method_analysis/pc_analysis.ipynb`

Notebook utiliser pour visualiser les solutions de la méthode de lissage par npyau à partir de l'ACP : pour passer d'une grille PC1-PC2 à une grille WS-SWH, en mettant les autre variables à leur valeur moyenne.

### 12. `neural_network/neural_network_sinthetic_data.ipynb`

Etude du SSB via les réseaux de neurones, avec delta_ssh dans le fonction de perte construire à partir des données synthétiques du modèle paramétrique 2D BM4 du SSB.

### 13. `neural_network/neural_network_sinthetic_data.ipynb`

Etude du SSB via les réseaux de neurones, avec delta_ssh provenant des données réelles comme WS et SWH.

### 14. `maj_tab/*.cmd`

fichiers commande pour mettre à jour les tables à partir des composantes principales


### 15. `notebook/*.ipynb`

anciens notebooks pour faire des tests, etc.