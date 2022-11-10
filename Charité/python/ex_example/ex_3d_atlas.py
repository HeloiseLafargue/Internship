"""
3d example with deformetrica
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
import matplotlib.gridspec as gridspec
import deformetrica as dfca


#matplotlib inline
#config InlineBackend.figure_format = 'retina'

data_path = '/home/icm-admin/Documents/Internship/data/examples/examples/'
data_base = os.path.join(data_path, 'registration/landmark/3d/bundles_cortico/data/')  # clean concatenation of 2 pathways 

vtk_files = glob.glob(data_base + "*putamen" + "*.vtk")  # list of the files' pathways (for putamen)

figsize = 5
f = plt.figure(figsize=(len(vtk_files) * figsize, 1 * figsize))
#gs = gridspec.GridSpec(1, len(vtk_files))  # separation of the figure into different plot areas

for i, vtk_file in enumerate(vtk_files):  
    # ax = plt.subplget_test_dataot(gs[0, i])  # creation of the axes for the considered plot area of the gridspec
    # color = cmap(i % 10)[:3]
    # ax = plt.axes(projection='3d')
    ax = f.add_subplot(1, len(vtk_files), i+1, projection='3d')
    
    #vtk_file = vtk_files[0]
    m = re.findall(r".*\/(.*)\..*", vtk_file)  # list which contains the name  of the considered file
    target_id = m[0]
    target_points__raw, _, target_connectivity__raw = dfca.io.DeformableObjectReader.read_file(vtk_file, extract_connectivity=True)
    # return: points, dimension, connectivity
    # if extract_connectivity=True, returns a third argument: the table of lines (connectivity)
    
    p = target_points__raw  # table of the points coordinates
    c = target_connectivity__raw    # lines table (first column: index of the starting point ; second column: index of the stage point ; third column : index of the ending point)
    
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
import deformetrica as dfca

data_path = '/home/icm-admin/Documents/Internship/data/examples/examples/'
data_base = os.path.join(data_path, 'registration/landmark/3d/bundles_cortico/data/')

iteration_status_dictionaries = []

def estimator_callback(status_dict):
    iteration_status_dictionaries.append(status_dict)
    return True

###############################################################################
#                        ''Using python dictionnaries''
###############################################################################

# set the data, model, parameters (transcription of the xml files into dictionnaries)
dataset_specifications = {
    'dataset_filenames': [
        [{#'bundle': os.path.join(data_base, 'subject_bundle.vtk'),
        'putamen': os.path.join(data_base, 'subject_putamen.vtk')}]],
    'subject_ids': ['subj1']
}

template_specifications = {
    # 'bundle': {'deformable_object_type': 'polyline',
    #           'kernel_type': 'keops', 'kernel_width': 11,
    #           'noise_std': 1.0,
    #           'filename': os.path.join(data_base, 'bundle_prototype.vtk'),
    #           'attachment_type': 'varifold'},
    'putamen': {'deformable_object_type': 'surfacemesh',
                'kernel_type': 'keops', 'kernel_width': 11,
              'noise_std': 0.1,
              'filename': os.path.join(data_base, 'putamen_prototype.vtk'),
              'attachment_type': 'varifold'}
}
estimator_options={'optimization_method_type': 'ScipyLBFGS', 'callback': estimator_callback}

# instantiate a Deformetrica object
deformetrica = dfca.Deformetrica(output_dir='output', verbosity='INFO')

#perform a deterministic atlas estimation
model = deformetrica.estimate_deterministic_atlas(template_specifications, dataset_specifications,
                                                estimator_options=estimator_options,
                                                  model_options={'deformation_kernel_type': 'keops', 'deformation_kernel_width': 15, 'dtype': 'float32'})


###############################################################################
#                          ''Using XmlParameters''
###############################################################################

# arg = dfca.io.XmlParameters() # creation of the XmlParameters object

# model_path =os.path.join(data_path, 'registration/landmark/3d/bundles_cortico/model.xml')
# dataset_path =os.path.join(data_path, 'registration/landmark/3d/bundles_cortico/data_set.xml')
# opt_param_path =os.path.join(data_path, 'registration/landmark/3d/bundles_cortico/optimization_parameters.xml')

# arg.read_all_xmls(model_path, dataset_path, opt_param_path) # reading of the 3 xml files

# template_specifications_xml = arg.template_specifications # access to the model dictionnarie of arg
# dataset_specifications_xml = dfca.io.get_dataset_specifications(arg) # same for data
# estimator_options_xml = dfca.io.get_estimator_options(arg) # same for estimator

# estimator_options_xml.update({'callback': estimator_callback}) # add a key to the dictinnarie to update iteration_status_dictionnaries

# # instantiate a Deformetrica object
# deformetrica = dfca.Deformetrica(output_dir='output', verbosity='INFO')

# #perform a deterministic atlas estimation
# model = deformetrica.estimate_deterministic_atlas(template_specifications_xml, dataset_specifications_xml,
#                                                 estimator_options=estimator_options_xml,
#                                                   model_options={'deformation_kernel_type': 'keops', 'deformation_kernel_width': 15, 'dtype': 'float32'})




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
y =  [it_data['current_log_likelihood'] for it_data in iteration_status_dictionaries]

# plot log-likelihood
f = plt.figure()
plt.plot(x, y, label='log_likelihood')
# plt.plot(x, [it_data['current_attachment'] for it_data in iteration_status_dictionaries], label='attachment')
# plt.plot(x, [it_data['current_regularity'] for it_data in iteration_status_dictionaries], label='regularity')

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
path_to_template__ini = template_specifications['putamen']['filename']
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
    path_to_target__raw = dataset_specifications['dataset_filenames'][i][0]['putamen']
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
                    ,'g') # same for y-coordinates
            
    if c.shape[1] == 3 :
        # plot the mesh : triangular mesh
        for k in range(len(c)):
            # plot the line between the starting point and the stage point
            ax.plot3D([p[c[k, 0]][0], p[c[k, 1]][0]], # table of the x-coordinates (first raw: x-coordinate of point where a line begins ; second raw: x-coordinate of point where the line ends)
                    [p[c[k, 0]][1], p[c[k, 1]][1]],  # same for y-coordinates
                    [p[c[k, 0]][2], p[c[k, 1]][2]]  # same for z-coordinates
                    ,'g') # same for y-coordinates
            # plot the line between the etape point and the ending point
            ax.plot3D([p[c[k, 1]][0], p[c[k, 2]][0]],
                    [p[c[k, 1]][1], p[c[k, 2]][1]], 
                    [p[c[k, 1]][2], p[c[k, 2]][2]]
                    ,'g')
            # plot the line between the starting point and the ending point
            ax.plot3D([p[c[k, 0]][0], p[c[k, 2]][0]],
                    [p[c[k, 0]][1], p[c[k, 2]][1]], 
                    [p[c[k, 0]][2], p[c[k, 2]][2]]
                    ,'g')
    
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
                    , 'k') # same for y-coordinates
            
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
    
plt.style.use('default')
plt.show()


