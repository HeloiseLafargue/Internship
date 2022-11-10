"""
Created on July 2022

Principal Geodesic Analysis with Deformetrica

@requirements: main directory with a folder 'data' containing the data and the 
template files (.vtk or .stl)

@input: 
	- data_path : path of the main directory
    - obj : name of the object ('LV')
    - data_specification : 
        filename and 'age' of the object for each subject
        subject_ids : list of the subject names (arbitrary)
	- template: filename and type

@author: Heloise LAFARGUE
"""

## IMPORT AND RUN DEFORMETRICA

import os
import glob
import deformetrica as dfca
import pyvista as pv


data_path = os.path.abspath('/home/icm-admin/Documents/Internship/data/TimeSeries_LV/')
data_base = os.path.join(data_path, 'data/')
output_path = os.path.join(data_path, 'output/output_geodesic_analysis')

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
    'visit_ages': [[1.0], [2.0]],
    'dataset_filenames': [
        [{'obj': os.path.join(data_base, 'Subject01_t01.vtk')}],
        [{'obj': os.path.join(data_base, 'Subject01_t02.vtk')}]
        ],
    'subject_ids': ['t1', 't2']
}
template_specifications = {
      'obj': {'deformable_object_type': 'surfacemesh',
             'kernel_type': 'torch', 'kernel_width': 5,
             'noise_std': 1.0,
             'filename': os.path.join(data_base, 'Subject01_t03.vtk'),
             'attachment_type': 'varifold',
             'noise_variance_prior_scale_std': None,
             'noise_variance_prior_normalized_dof': 0.01}
}
estimator_options= {'memory_length': 10,
     'freeze_template': True,   # by default the template is frozen during a geodesic regression
     'max_line_search_iterations': 10,
     'optimized_log_likelihood': 'complete',
     'optimization_method_type': 'scipylbfgs',
     'max_iterations': 100,
     'convergence_tolerance': 0.0001,
     'print_every_n_iters': 1, 'save_every_n_iters': 1,
     'state_file': os.path.join(output_path, 'geodesic-state.p'),
     'load_state_file': False,
     'callback': estimator_callback}

# instantiate a Deformetrica object
deformetrica = dfca.Deformetrica(output_dir=output_path, verbosity='INFO')

# perform a deterministic atlas estimation
model = deformetrica.estimate_principal_geodesic_analysis(template_specifications, dataset_specifications,
    estimator_options=estimator_options,
    model_options={'deformation_kernel_type': 'keops', 'deformation_kernel_width': 9, 
                   'dtype': 'float32', 'dimension':3, 'latent_space_dimension' : 3, # working in 3 dimension
                   'model_type' : 'PrincipalGeodesicAnalysis'})

# VTK2STL 
output_files = glob.glob(output_path + "*.vtk")

for output_file in output_files: 
    filename =  output_file.split('.')[0]
    mesh2 = pv.read(output_file)
    mesh2.save(filename + ".stl",binary=False)