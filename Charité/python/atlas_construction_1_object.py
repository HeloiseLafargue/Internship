"""
Created on July 2022

Atlas construction with Deformetrica for one object
(estimation for various data subject with only one object for each one)

@requirements: main directory with a folder 'data' containing the data and the 
template files (.vtk or .stl)

@input: 
	- data_path : path of the main directory
    - object : name of the object
	- template : name of the template (without the extension)

@author: Heloise LAFARGUE

_______________________________________________________________________________
Section 0 : plot the input -> specify
            - data_path : path of the main directory
            
Section 1 : run the Deformetrica simulation -> specify 
            - data_path : path of the main directory
            - object_name : the name of the object ('LA')
            - template_filename : filename without extension 
            ('LA_Sphere' if the template is 'LA_Sphere.vtk')
            
Section 2 : plot the log-likelihood -> 
                run the section 1 before

Section 3 : plot the result output, comparison and momenta ->
                run the section 1 before
                _____________________________________________
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

data_path = os.path.abspath('/home/icm-admin/Documents/Internship/data/realLAGeometry/')
data_base = os.path.join(data_path, 'data/') # clean concatenation of 2 pathways 

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
    target_points__raw, _, target_connectivity__raw = dfca.io.DeformableObjectReader.read_file(
        vtk_file, extract_connectivity=True)
    # return: points, dimension, connectivity
    # if extract_connectivity=True, returns a 3rd argument: the table of lines (connectivity)
    
    p = target_points__raw  # table of the points coordinates
    c = target_connectivity__raw    # lines table (first column: index of the starting point ; second column: index of the stage point ; third column : index of the ending point)
    
    if c.shape[1] == 2 :
        # plot the mesh : segments
        for k in range(len(c)):
            # plot the line between the starting point and the ending point
            ax.plot3D([p[c[k, 0]][0], p[c[k, 1]][0]], # table of the x-coordinates (first raw: x-coordinate of point where a line begins ; second raw: x-coordinate of point where the line ends)
                    [p[c[k, 0]][1], p[c[k, 1]][1]],  # same for y-coordinates
                    [p[c[k, 0]][2], p[c[k, 1]][2]]  # same for z-coordinates
                    ) # same for y-coordinates
            
    if c.shape[1] == 3 :
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




#%%############################################################################
#
#                        ''IMPORT AND RUN DEFORMETRICA''
#
###############################################################################

import os
import glob
import deformetrica as dfca
import pyvista as pv

data_path = os.path.abspath('/home/icm-admin/Documents/Internship/data/realLAGeometry/')
data_base = os.path.join(data_path, 'data/') # clean concatenation of 2 pathways 


# STL2VTK   
stl_files = glob.glob(data_base + "*.stl")
for stl_file in stl_files: 
    filename =  stl_file.split('.')[0]
    mesh = pv.read(stl_file)
    mesh.save(filename + ".vtk",binary=False)
vtk_files = glob.glob(data_base + "*.vtk")

# estimator callback to save and later plot the log-likelihood values
iteration_status_dictionaries = []
def estimator_callback(status_dict):
    iteration_status_dictionaries.append(status_dict)
    return True


# Set the parameters using python dictionnaries


# name of the object
object_name = 'LA'
# choice of the template
template_filename = 'LA_Sphere' # filename without extension
template_path = os.path.join(data_base, template_filename + '.vtk') # template path

data_files = [] # list of the data, without the template
sub_ids = [] # list of filename
for data_file in vtk_files:
    if data_file != template_path:
        dict_data = {object_name : data_file}
        data = [dict_data]
        data_files.append(data)
        sub_id = data_file.split('/')[-1].split('.')[0] 
        sub_ids.append(sub_id)

# set the data, model, parameters dictionnaries
dataset_specifications = {
    'dataset_filenames': data_files,
    'subject_ids': sub_ids
}

template_specifications = {
    object_name : {'deformable_object_type': 'surfacemesh',
                'kernel_type': 'torch', 'kernel_width': 5, 'noise_std': 0.1,
                'filename': template_path,
                'attachment_type': 'varifold'}
}
# Scipy method
estimator_options={'optimization_method_type': 'ScipyLBFGS', 'max_iterations': 90, 
                   'convergence_tolerance':10**(-100), 'max_line_search_iterations':20, 
                   'callback': estimator_callback}
# GradientAscent method
# estimator_options={'optimization_method_type': 'GradientAscent', 'initial_step_size': 1.,
#                     'max_iterations': 90, 'max_line_search_iterations': 10, 
#                     'convergence_tolerance':10**(-6),'callback': estimator_callback}


# create the output dir if doesn't exists and delete the previous files
output_path = os.path.join(data_path, 'output/')
filelist = glob.glob(os.path.join(output_path, "*"))
for f in filelist:
    os.remove(f)
isExist = os.path.exists(output_path)
os.makedirs(output_path, exist_ok=isExist)

# instantiate a Deformetrica object
deformetrica = dfca.Deformetrica(output_dir=output_path, verbosity='INFO')

# perform a deterministic atlas estimation
model = deformetrica.estimate_deterministic_atlas(template_specifications, dataset_specifications,
    estimator_options=estimator_options,
    model_options={'deformation_kernel_type': 'keops', 'deformation_kernel_width': 9, 'dtype': 'float32'})

# VTK2STL 
output_files = glob.glob(output_path + "*.vtk")

for output_file in output_files: 
    filename =  output_file.split('.')[0]
    mesh2 = pv.read(output_file)
    mesh2.save(filename + ".stl",binary=False)

#%%############################################################################
# 
#                          ''PLOT LOG-LIKEKIHOOD''
#
###############################################################################

import numpy as np
import matplotlib.pyplot as plt
#matplotlib inline
#config InlineBackend.figure_format = 'retina'

# print available saved status keys
print(iteration_status_dictionaries[-1].keys())
# print(iteration_status_dictionaries[-1]['gradient'].keys())

max_iterations = len(iteration_status_dictionaries) # for the len of x
x = np.arange(1, max_iterations+1)
y =  [abs(it_data['current_log_likelihood']) for it_data in iteration_status_dictionaries]

# plot log-likelihood
f = plt.figure()
plt.plot(x, y, label='log_likelihood')
# plt.plot(x, [it_data['current_attachment'] for it_data in iteration_status_dictionaries], label='attachment')
# plt.plot(x, [it_data['current_regularity'] for it_data in iteration_status_dictionaries], label='regularity')

plt.yscale('log')

plt.xticks(x)

plt.style.use('default')
plt.legend()
plt.show()


#%%############################################################################
#
#                       ''PLOT RESULTING TEMPLATES''
#
###############################################################################

####
#### LOAD RELEVANT INPUT DATA
####

import deformetrica as dfca

#for t in template_specifications.items():
#    path_to_template__ini = t[1]['filename']
path_to_template__ini = template_specifications[object_name]['filename']
template_points__ini, dimension, template_connectivity__ini = dfca.io.DeformableObjectReader.read_file(path_to_template__ini, extract_connectivity=True)

####
#### LOAD RELEVANT OUTPUT DATA
####
    
fixed_effects = model.fixed_effects
    
template_points__est = fixed_effects['template_data']['landmark_points']
control_points__est = fixed_effects['control_points']
momenta__est = fixed_effects['momenta']

####
#### PLOT INITIAL AND ESTIMATED TEMPLATES
####
    
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import cm
#%matplotlib inline
#%config InlineBackend.figure_format = 'retina'
    
figsize = 5
f = plt.figure(figsize=(3*figsize, 1*figsize))
gs = gridspec.GridSpec(1, 3)
    
############################# Initial template ################################

ax = plt.subplot(gs[0, 0], projection='3d')
p = template_points__ini
c = template_connectivity__ini

if c.shape[1] == 2 :
    # plot the mesh : linear mesh
    for k in range(len(c)):
        # plot the line between the starting point and the ending point
        ax.plot3D([p[c[k, 0]][0], p[c[k, 1]][0]], # table of the x-coordinates (first raw: x-coordinate of point where a line begins ; second raw: x-coordinate of point where the line ends)
                [p[c[k, 0]][1], p[c[k, 1]][1]],  # same for y-coordinates
                [p[c[k, 0]][2], p[c[k, 1]][2]]  # same for z-coordinates
                ,'k') # same for y-coordinates
        
if c.shape[1] == 3 :
    # plot the mesh : triangular mesh
    for k in range(len(c)):
        # plot the line between the starting point and the stage point
        ax.plot3D([p[c[k, 0]][0], p[c[k, 1]][0]], # table of the x-coordinates (first raw: x-coordinate of point where a line begins ; second raw: x-coordinate of point where the line ends)
                [p[c[k, 0]][1], p[c[k, 1]][1]],  # same for y-coordinates
                [p[c[k, 0]][2], p[c[k, 1]][2]]  # same for z-coordinates
                ,'k') # same for y-coordinates
        # plot the line between the etape point and the ending point
        ax.plot3D([p[c[k, 1]][0], p[c[k, 2]][0]],
                [p[c[k, 1]][1], p[c[k, 2]][1]], 
                [p[c[k, 1]][2], p[c[k, 2]][2]]
                ,'k')
        # plot the line between the starting point and the ending point
        ax.plot3D([p[c[k, 0]][0], p[c[k, 2]][0]],
                [p[c[k, 0]][1], p[c[k, 2]][1]], 
                [p[c[k, 0]][2], p[c[k, 2]][2]]
                ,'k')
        
ax.set_title('Initial template')
    

############################ Estimated template ###############################

ax = plt.subplot(gs[0, 1], projection='3d')
p = template_points__est
if c.shape[1] == 2 :
    # plot the mesh : linear mesh
    for k in range(len(c)):
        # plot the line between the starting point and the ending point
        ax.plot3D([p[c[k, 0]][0], p[c[k, 1]][0]], # table of the x-coordinates (first raw: x-coordinate of point where a line begins ; second raw: x-coordinate of point where the line ends)
                [p[c[k, 0]][1], p[c[k, 1]][1]],  # same for y-coordinates
                [p[c[k, 0]][2], p[c[k, 1]][2]]  # same for z-coordinates
                ,'k') # same for y-coordinates
        
if c.shape[1] == 3 :
    # plot the mesh : triangular mesh
    for k in range(len(c)):
        # plot the line between the starting point and the stage point
        ax.plot3D([p[c[k, 0]][0], p[c[k, 1]][0]], # table of the x-coordinates (first raw: x-coordinate of point where a line begins ; second raw: x-coordinate of point where the line ends)
                [p[c[k, 0]][1], p[c[k, 1]][1]],  # same for y-coordinates
                [p[c[k, 0]][2], p[c[k, 1]][2]]  # same for z-coordinates
                ,'k') # same for y-coordinates
        # plot the line between the etape point and the ending point
        ax.plot3D([p[c[k, 1]][0], p[c[k, 2]][0]],
                [p[c[k, 1]][1], p[c[k, 2]][1]], 
                [p[c[k, 1]][2], p[c[k, 2]][2]]
                ,'k')
        # plot the line between the starting point and the ending point
        ax.plot3D([p[c[k, 0]][0], p[c[k, 2]][0]],
                [p[c[k, 0]][1], p[c[k, 2]][1]], 
                [p[c[k, 0]][2], p[c[k, 2]][2]]
                ,'k')
ax.set_title('Estimated template')
  
##################### Estimated template and momenta ##########################

ax = plt.subplot(gs[0, 2], projection='3d')
x = control_points__est
if c.shape[1] == 2 :
    # plot the mesh : linear mesh
    for k in range(len(c)):
        # plot the line between the starting point and the ending point
        ax.plot3D([p[c[k, 0]][0], p[c[k, 1]][0]], # table of the x-coordinates (first raw: x-coordinate of point where a line begins ; second raw: x-coordinate of point where the line ends)
                [p[c[k, 0]][1], p[c[k, 1]][1]],  # same for y-coordinates
                [p[c[k, 0]][2], p[c[k, 1]][2]]  # same for z-coordinates
                ,'k') # same for y-coordinates
        
if c.shape[1] == 3 :
    # plot the mesh : triangular mesh
    for k in range(len(c)):
        # plot the line between the starting point and the stage point
        ax.plot3D([p[c[k, 0]][0], p[c[k, 1]][0]], # table of the x-coordinates (first raw: x-coordinate of point where a line begins ; second raw: x-coordinate of point where the line ends)
                [p[c[k, 0]][1], p[c[k, 1]][1]],  # same for y-coordinates
                [p[c[k, 0]][2], p[c[k, 1]][2]]  # same for z-coordinates
                ,'k') # same for y-coordinates
        # plot the line between the etape point and the ending point
        ax.plot3D([p[c[k, 1]][0], p[c[k, 2]][0]],
                [p[c[k, 1]][1], p[c[k, 2]][1]], 
                [p[c[k, 1]][2], p[c[k, 2]][2]]
                ,'k')
        # plot the line between the starting point and the ending point
        ax.plot3D([p[c[k, 0]][0], p[c[k, 2]][0]],
                [p[c[k, 0]][1], p[c[k, 2]][1]], 
                [p[c[k, 0]][2], p[c[k, 2]][2]]
                ,'k')
cmap = cm.get_cmap('tab10')
for i, m in enumerate(momenta__est):
    color = cmap(i % 10)[:3]
    ax.quiver(x[:,0], x[:,1], x[:,2], m[:,0], m[:,1], m[:,2], color=color)
ax.set_title('Estimated template and momenta')

####
#### PLOT RAW VERSUS RECONSTRUCTED DATA
####

import torch 

figsize = 3
#f = plt.figure(figsize=(5*figsize, 1*figsize))
f = plt.figure()
gs = gridspec.GridSpec(1, 5)

for i, momentum__est in enumerate(momenta__est): 
    #ax = plt.subplot(gs[0, i])
    ax = plt.subplot(projection='3d')
    color = cmap(i % 10)[:3]
  
    # Load and plot raw target. 
    path_to_target__raw = dataset_specifications['dataset_filenames'][i][0][object_name]
    target_id = dataset_specifications['subject_ids'][i]
    target_points__raw, _, target_connectivity__raw = dfca.io.DeformableObjectReader.read_file(path_to_target__raw, extract_connectivity=True)

    p = target_points__raw
    c = target_connectivity__raw
    
    if c.shape[1] == 2 :
        # plot the mesh : linear mesh
        for k in range(len(c)):
            # plot the line between the starting point and the ending point
            ax.plot3D([p[c[k, 0]][0], p[c[k, 1]][0]], # table of the x-coordinates (first raw: x-coordinate of point where a line begins ; second raw: x-coordinate of point where the line ends)
                    [p[c[k, 0]][1], p[c[k, 1]][1]],  # same for y-coordinates
                    [p[c[k, 0]][2], p[c[k, 1]][2]]  # same for z-coordinates
                    ,'k') # same for y-coordinates
            
    if c.shape[1] == 3 :
        # plot the mesh : triangular mesh
        for k in range(len(c)):
            # plot the line between the starting point and the stage point
            ax.plot3D([p[c[k, 0]][0], p[c[k, 1]][0]], # table of the x-coordinates (first raw: x-coordinate of point where a line begins ; second raw: x-coordinate of point where the line ends)
                    [p[c[k, 0]][1], p[c[k, 1]][1]],  # same for y-coordinates
                    [p[c[k, 0]][2], p[c[k, 1]][2]]  # same for z-coordinates
                    ,'k') # same for y-coordinates
            # plot the line between the etape point and the ending point
            ax.plot3D([p[c[k, 1]][0], p[c[k, 2]][0]],
                    [p[c[k, 1]][1], p[c[k, 2]][1]], 
                    [p[c[k, 1]][2], p[c[k, 2]][2]]
                    ,'k')
            # plot the line between the starting point and the ending point
            ax.plot3D([p[c[k, 0]][0], p[c[k, 2]][0]],
                    [p[c[k, 0]][1], p[c[k, 2]][1]], 
                    [p[c[k, 0]][2], p[c[k, 2]][2]]
                    ,'k')
    
    ax.set_title(target_id)
  
    # Compute and plot the reconstruction of the target. 
    model.exponential.set_initial_momenta(torch.from_numpy(momentum__est).to(torch.float32))
    model.exponential.update()
    target_points__rec = model.exponential.get_template_points()['landmark_points'].detach().cpu().numpy()
  
    p = target_points__rec
    c = template_connectivity__ini
    
    if c.shape[1] == 2 :
        # plot the mesh : linear mesh
        for k in range(len(c)):
            # plot the line between the starting point and the ending point
            ax.plot3D([p[c[k, 0]][0], p[c[k, 1]][0]], # table of the x-coordinates (first raw: x-coordinate of point where a line begins ; second raw: x-coordinate of point where the line ends)
                    [p[c[k, 0]][1], p[c[k, 1]][1]],  # same for y-coordinates
                    [p[c[k, 0]][2], p[c[k, 1]][2]]  # same for z-coordinates
                    ) # same for y-coordinates
            
    if c.shape[1] == 3 :
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
                    )
    
plt.style.use('default')
plt.show()


