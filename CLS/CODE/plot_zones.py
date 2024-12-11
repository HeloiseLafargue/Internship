import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import hsv_to_rgb
from matplotlib.patches import Rectangle
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

def main():
    zones = ['North Pacific', 'Equator', 'South Pacific', 'North West Pacific', 'South East Pacific', 'Indian Ocean', 'Wide Tropics']
    latitudes = [[0, 60], [-20, 20], [-60, 0], [20, 70], [-60,-10], [-20, 30], [-30,30]]
    longitudes = [
        [[-180, -100], [120, 180]],  # PacifiqueNord
        [[-180, -20], [140, 180]],  # Equateur
        [[-180, -80], [140, 180]],  # PacifiqueSud
        [120, 180],  # PacifiqueJapon
        [-120, -70],  # PacifiqueSudEst
        [40, 100],  # OceanIndien
        [-162, 20] # Tropique Large
    ]

    fig, ax = plt.subplots(figsize=(15, 10), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
    colors = generate_distinct_colors(len(zones))
    
    for i, (zone, lat_range, lon_ranges) in enumerate(zip(zones, latitudes, longitudes)):
        color = colors[i]
        alpha = 0.4  # Niveau de transparence
        label_added = False  # Flag pour s'assurer qu'on ajoute le label une seule fois
        if isinstance(lon_ranges[0], list):  # Gérer les plages de longitude discontinues
            for lon_range in lon_ranges:
                ax.add_patch(Rectangle((lon_range[0], lat_range[0]), lon_range[1]-lon_range[0], lat_range[1]-lat_range[0], 
                                       color=color, alpha=alpha, transform=ccrs.PlateCarree(), 
                                       label=zone if not label_added else ""))
                label_added = True
        else:
            ax.add_patch(Rectangle((lon_ranges[0], lat_range[0]), lon_ranges[1]-lon_ranges[0], lat_range[1]-lat_range[0], 
                                   color=color, alpha=alpha, transform=ccrs.PlateCarree(), label=zone))

    plt.legend(loc='lower left')
    ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
    ax.set_xticks([-180, -120, -60, 0, 60, 120, 180], crs=ccrs.PlateCarree())
    ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    plt.title("Specific regions studied to verify the local stability of PCA")
    plt.savefig('results/local_zones_plot.png', dpi=300)
    plt.show()

def generate_distinct_colors(n):
    """Générer n couleurs distinctes."""
    hsv_colors = [(i / n, 0.7, 0.9) for i in range(n)]  # Saturation et Value fixes, Hue varie
    rgb_colors = [hsv_to_rgb(color) for color in hsv_colors]
    return rgb_colors

if __name__ == "__main__":
    main()
