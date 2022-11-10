"""
Created on July 2022

Geodesic regression with Deformetrica

@requirements: main directory with a folder 'data' containing the data and the 
template files (.vtk or .stl)

@input: 
	- data_path : path of the main directory
    - obj : name of the object ('LV')
    - data_specification : filename and 'age' of the object
	- template: filename and type, you can choose any .vtk file in the folder,
    the template unused because it is frozen for geodesic regression

@author: Heloise LAFARGUE
"""

## IMPORT AND RUN DEFORMETRICA

import os
import glob
import deformetrica as dfca
import pyvista as pv


data_path = os.path.abspath('/home/icm-admin/Documents/Internship/data/TimeSeries_LV/')
data_base = os.path.join(data_path, 'data/')
output_path = os.path.join(data_path, 'output/output_geodesic_regression/')

# STL2VTK   
stl_files = glob.glob(data_base + "*.stl")
for stl_file in stl_files: 
    filename =  stl_file.split('.')[0]
    mesh = pv.read(stl_file)
    mesh.save(filename + ".vtk",binary=False)
vtk_files = glob.glob(data_base + "*.vtk")

# create the output dir if doesn't exists and delete the previous state files
filelist = glob.glob(output_path + "*.log")
for f in filelist:
    os.remove(f)
isExist = os.path.exists(output_path)
os.makedirs(output_path, exist_ok=isExist)

# estimator callback to save and later plot the log-likelihood values
iteration_status_dictionaries = []

def estimator_callback(status_dict):
    iteration_status_dictionaries.append(status_dict)
    return True

# set the data, model, parameters dictionnaries
obj = 'LV'
dataset_specifications = {
    'visit_ages': [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0,
                    12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0,
                    22.0, 23.0, 24.0, 25.0
                    ]],
    'dataset_filenames': [[
        {obj: os.path.join(data_base, 'Subject01_t01.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t02.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t03.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t04.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t05.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t06.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t07.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t08.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t09.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t10.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t11.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t12.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t13.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t14.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t15.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t16.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t17.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t18.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t19.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t20.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t21.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t22.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t23.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t24.vtk')},
        {obj: os.path.join(data_base, 'Subject01_t25.vtk')}
        ]],
    'subject_ids': ['subj']
}
template_specifications = {
      obj: {'deformable_object_type': 'surfacemesh',
              'kernel_type': 'torch', 'kernel_width': 5,
              'noise_std': 1.0,
              'filename': os.path.join(data_base, 'Subject01_t01.vtk'),
              'attachment_type': 'varifold',
              'noise_variance_prior_scale_std': None,
              'noise_variance_prior_normalized_dof': 0.01}
}
estimator_options= {
     'freeze_template': True,   # by default the template is frozen during a geodesic regression
     'max_line_search_iterations': 10,
     'initial_step_size': 1e-09,
     'scale_initial_step_size': True,
     'line_search_shrink': 0.5,
     'line_search_expand': 1.5,
     'optimization_method_type': 'scipylbfgs',
     'max_iterations': 50,
     'convergence_tolerance': 0.00000001,
     'print_every_n_iters': 1, 'save_every_n_iters': 5,
     'callback': estimator_callback}

# instantiate a Deformetrica object
deformetrica = dfca.Deformetrica(output_dir=output_path, verbosity='INFO')

# perform a deterministic atlas estimation
model = deformetrica.estimate_geodesic_regression(template_specifications, dataset_specifications,
    estimator_options=estimator_options,
    model_options={'deformation_kernel_type': 'keops', 'deformation_kernel_width': 9, 
                   'dtype': 'float32', 'dimension': 3, 'latent_space_dimension' : 3, # working in 3D
                   'model_type' : 'GrodesicRegression'})

# VTK2STL 
output_files = glob.glob(output_path + "*.vtk")

for output_file in output_files: 
    filename =  output_file.split('.')[0]
    mesh2 = pv.read(output_file)
    mesh2.save(filename + ".stl",binary=False)
    

# rename the "flow" files so it is possible to open the files with the same 
# prefix as a group in Paraview and play the video
output_files = glob.glob(output_path + "*.vtk")

for output_file in output_files: 
        old_name = output_file.split('.')[0]
        new_name = old_name.split('__age')[0]      
        os.rename(output_file, new_name + ".vtk")
