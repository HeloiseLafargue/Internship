import os
import re
import deformetrica as dfca

vtk_file = os.path.abspath('/home/icm-admin/Documents/Internship/data/moreLA/data/Subject01_LA_elongated_PV.vtk')
    
m = re.findall(r".*\/(.*)\..*", vtk_file)  # list which contains the name  of the considered file
target_id = m[0]
target_points__raw, _, target_connectivity__raw = dfca.io.DeformableObjectReader.read_file(vtk_file, extract_connectivity=True)
    # return: points, dimension, connectivity
points = target_points__raw  # table of the points coordinates
c = target_connectivity__raw    # lines table (first column: index of the starting point ; second column: index of the stage point ; third column : index of the ending point)
    

x_coords = [p[0] for p in points]
y_coords = [p[1] for p in points]
z_coords = [p[2] for p in points]

_len = len(points)
centroid_x = sum(x_coords)/_len
centroid_y = sum(y_coords)/_len
centroid_z = sum(z_coords)/_len
barycenter = [centroid_x, centroid_y, centroid_z]

print(barycenter)
