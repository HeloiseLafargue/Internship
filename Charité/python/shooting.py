"""
Created on July 2022

Shooting with Deformetrica

@requirements: 
If control points and momenta corresponding to a deformation have been obtained, 
it is possible to shoot the corresponding deformation of obtain the flow of a 
shape under this deformation.

@input: 
	- data_path : path of the main directory
    - output_regression_path : path of the directory where the deformation have
    been obtained
    - initial_control_points_path : complete the filename of the control points
    - initial_momenta_path : complete the filename of the momenta
	- template: label ('LV'), filename and type ('surfacemesh')
    
@author: Heloise LAFARGUE
"""

## IMPORT AND RUN DEFORMETRICA
import os
import glob
import deformetrica as dfca

data_path = os.path.abspath('/home/icm-admin/Documents/Internship/data/TimeSeries_LV/')
data_base = os.path.join(data_path, 'data/')
output_regression_path = os.path.join(data_path, 'output/output_geodesic_regression/')
output_path = os.path.join(data_path, 'output/shooting/')

initial_control_points_path = os.path.join(output_regression_path, 'GeodesicRegression__EstimatedParameters__ControlPoints.txt')
initial_momenta_path = os.path.join(output_regression_path, 'GeodesicRegression__EstimatedParameters__Momenta.txt')

# set the template dictionnaries
template_specifications = {
      'LV': {'deformable_object_type': 'surfacemesh',
             'kernel_type': 'torch', 'kernel_width': 5,
             'noise_std': 1.0,
             'filename': os.path.join(data_base, 'Subject01_t01.vtk'),
             'attachment_type': 'varifold',
             'noise_variance_prior_scale_std': None,
             'noise_variance_prior_normalized_dof': 0.01
             }
}

# instantiate a Deformetrica object
deformetrica = dfca.Deformetrica(output_dir=output_path, verbosity='INFO')

# perform a deterministic atlas estimation
model = deformetrica.compute_shooting(template_specifications,
    model_options={'deformation_kernel_type': 'torch', 'deformation_kernel_width': 10.0, 
                   'dtype': 'float32', 'dimension':3,'model_type' : 'Shooting',
                   't0':0, 'tmin':0, 'tmax': 30,
                   'initial_control_points' : initial_control_points_path,
                   'initial_momenta' : initial_momenta_path})

# rename the "flow" files so it is possible to open the files with the same 
# prefix as a group in Paraview and play the video
output_files = glob.glob(output_path + "*.vtk")

for output_file in output_files: 
    old_name = output_file.split('.')[0]
    new_name = old_name.split('__age')[0]      
    os.rename(output_file, new_name + ".vtk")
