import subprocess
import sys

def main(dataset_name):
    zones = ["PacifiqueNord", "Equateur", "PacifiqueSud", "PacifiqueNordOuest", "PacifiqueSudEst", "OceanIndien", "TropiqueLarge"]
    latitudes = [[0, 60], [-20, 20], [-60, 0], [20, 70], [-60, -10], [-20, 30], [-30,30]]
    longitudes = [
        [[-180, -100], [120, 180]],
        [[-180, -20], [140, 180]],
        [[-180, -80], [140, 180]],
        [120, 180],
        [-120, -70],
        [40, 100],
        [-162, 20]
    ]

    for zone, lat, lon in zip(zones, latitudes, longitudes):
        args = ["python", "process_regional_dataset.py", dataset_name, zone, str(lat[0]), str(lat[1])]
        if isinstance(lon[0], list):  # Discontinuous longitude range
            for l in lon:
                args.extend([str(l[0]), str(l[1])])
        else:
            args.extend([str(lon[0]), str(lon[1])])
        subprocess.run(args)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dataset_name = sys.argv[1]
        main(dataset_name)
    else:
        print("Usage: python script.py <dataset_name>")
        print("Example: python script.py SAR")
