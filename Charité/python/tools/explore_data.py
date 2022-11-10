"""
Created on July 2022

Explore data with Deformetrica 

@requirements: main directory with a folder 'data' containing the data and 
template files (.vtk or .stl)

@input: 
	- data_path : path of the main directory

@author: Heloise LAFARGUE
"""

###############################################################################
#
#                               ''EXPLORE DATA''
#
###############################################################################

import os
import glob
import re
import numpy as np
import matplotlib.pyplot as plt
import deformetrica as dfca
import pyvista as pv

#data_base = '/home/icm-admin/Documents/Internship/data/realLAGeometry/data/'

def explore(data_base):

    # STL2VTK 
    stl_files = glob.glob(data_base + "*.stl")  
    for i, stl_file in enumerate(stl_files): 
        filename =  stl_file.split('.')[0]
        mesh = pv.read(stl_file)
        mesh.save(filename + ".vtk",binary=False)
    
    vtk_files = glob.glob(data_base + "*.vtk")  # list of the files' pathways
    
    figsize = 5
    f = plt.figure(figsize=(len(vtk_files) * figsize, 1 * figsize))
    
    for i, vtk_file in enumerate(vtk_files):  
        ax = f.add_subplot(1, len(vtk_files), i+1, projection='3d')
        
        m = re.findall(r".*\/(.*)\..*", vtk_file)  # list which contains the name  of the considered file
        target_id = m[0]
        target_points__raw, _, target_connectivity__raw = dfca.io.DeformableObjectReader.read_file(vtk_file, extract_connectivity=True)
        # return: points, dimension, connectivity
        # if extract_connectivity=True, returns a third argument: the table of lines (connectivity)
        
        p = target_points__raw  # table of the points coordinates
        c = target_connectivity__raw    # lines table (first column: index of the starting point ; second column: index of the stage point ; third column : index of the ending point)
        
        
        if c == None :
            # if the mesh is point clouds
            print("Error plot : Connectivity isn't linear or triangular for the file " + vtk_file)
            
        elif c.shape[1] == 2 :
            # plot the mesh : segments
            for k in range(len(c)):
                # plot the line between the starting point and the ending point
                ax.plot3D([p[c[k, 0]][0], p[c[k, 1]][0]], # table of the x-coordinates (first raw: x-coordinate of point where a line begins ; second raw: x-coordinate of point where the line ends)
                        [p[c[k, 0]][1], p[c[k, 1]][1]],  # same for y-coordinates
                        [p[c[k, 0]][2], p[c[k, 1]][2]]  # same for z-coordinates
                        ) # same for y-coordinates
                
        elif c.shape[1] == 3 :
            # plot the mesh : triangular mesh
            for k in range(len(c)):
                # plot the line between the starting point and the stage point
                ax.plot3D([p[c[k, 0]][0], p[c[k, 1]][0]], # table of the x-coordinates (first raw: x-coordinate of point where a line begins ; second raw: x-coordinate of point where the line ends)
                        [p[c[k, 0]][1], p[c[k, 1]][1]],  # same for y-coordinates
                        [p[c[k, 0]][2], p[c[k, 1]][2]]  # same for z-coordinates
                        ) # same for y-coordinates
                # plot the line between the etape point and the ending point
                ax.plot3D([p[c[k, 1]][0], p[c[k, 2]][0]],
                        [p[c[k, 1]][1], p[c[k, 2]][1]], 
                        [p[c[k, 1]][2], p[c[k, 2]][2]]
                        )
                # plot the line between the starting point and the ending point
                ax.plot3D([p[c[k, 0]][0], p[c[k, 2]][0]],
                        [p[c[k, 0]][1], p[c[k, 2]][1]], 
                        [p[c[k, 0]][2], p[c[k, 2]][2]]
                        ,'k')
                
        ax.set_title(target_id)
    
    plt.style.use('default')
    plt.show()

explore(data_base)



# from explore_data import  explore 
# data_base = os.path.abspath('/home/icm-admin/Documents/Internship/data/realLAGeometry/data/')
# explore(data_base)