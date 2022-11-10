"""
2d example with deformetrica
"""


## EXPLORE DATA

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

data_base = os.path.join(data_path, 'regression/landmark/2d/skulls/data/')  # clean concatenation of 2 pathways 

vtk_files = glob.glob(data_base + "*.vtk")  # list of the files' pathways

figsize = 5
f = plt.figure(figsize=(5 * figsize, 1 * figsize))
gs = gridspec.GridSpec(1, len(vtk_files))  # separation of the figure into different plot areas

for i, vtk_file in enumerate(vtk_files):  
    ax = plt.subplot(gs[0, i])  # creation of the axes for the considered plot area of the gridspec
    # color = cmap(i % 10)[:3]

    m = re.findall(r".*\/(.*)\..*", vtk_file)  # list which contains the name  of the considered file
    target_id = m[0]
    target_points__raw, _, target_connectivity__raw = dfca.io.DeformableObjectReader.read_file(vtk_file, extract_connectivity=True)
    # return: points, dimension, connectivity
    # if extract_connectivity=True, returns a third argument: the table of lines (connectivity)
    
    p = target_points__raw  # table of the points coordinates
    c = target_connectivity__raw    # lines table (first column: index of the starting point ; second column: index of the ending point)

    ax.plot([p[c[:, 0]][:, 0], p[c[:, 1]][:, 0]], # table of the x-coordinates (first raw: x-coordinates of points where a line begins ; second raw: x-coordinates of points where the line ends)
            [p[c[:, 0]][:, 1], p[c[:, 1]][:, 1]], # same for y-coordinates
            'k', linewidth=2)  # all the points from the same column are linked together (number of columns = number of lines)
    ax.set_title(target_id)

plt.style.use('default')
plt.show()


#%% 
## IMPORT AND RUN DEFORMETRICA

import os
import deformetrica as dfca

data_path = '/home/icm-admin/Documents/Internship/data/examples/examples/'
data_base = os.path.join(data_path, 'atlas/landmark/2d/skulls/data/')

iteration_status_dictionaries = []

def estimator_callback(status_dict):
    iteration_status_dictionaries.append(status_dict)
    return True

# instantiate a Deformetrica object
deformetrica = dfca.Deformetrica(output_dir='output', verbosity='INFO')

dataset_specifications = {
    'dataset_filenames': [
        [{'skull': os.path.join(data_base, 'skull_australopithecus.vtk')}],
        [{'skull': os.path.join(data_base, 'skull_erectus.vtk')}],
        [{'skull': os.path.join(data_base, 'skull_habilis.vtk')}],
        [{'skull': os.path.join(data_base, 'skull_neandertalis.vtk')}],
        [{'skull': os.path.join(data_base, 'skull_sapiens.vtk')}]],
    'subject_ids': ['australopithecus', 'erectus', 'habilis', 'neandertalis', 'sapiens'],
}
template_specifications = {
    'skull': {'deformable_object_type': 'polyline',
              'kernel_type': 'torch', 'kernel_width': 20.0,
              'noise_std': 1.0,
              'filename': os.path.join(data_base, 'template.vtk'),
              'attachment_type': 'varifold'}
}
estimator_options={'optimization_method_type': 'GradientAscent', 'initial_step_size': 1.,
                    'max_iterations': 25, 'max_line_search_iterations': 10, 'callback': estimator_callback}


# perform a deterministic atlas estimation
model = deformetrica.estimate_deterministic_atlas(template_specifications, dataset_specifications,
                                                estimator_options=estimator_options,
                                                model_options={'deformation_kernel_type': 'torch', 'deformation_kernel_width': 40.0, 'dtype': 'float32'})




#%%
## PLOT LOG-LIKEKIHOOD

import numpy as np
import matplotlib.pyplot as plt
#matplotlib inline
#config InlineBackend.figure_format = 'retina'

# print available saved status keys
print(iteration_status_dictionaries[-1].keys())
# print(iteration_status_dictionaries[-1]['gradient'].keys())

x = np.arange(1, estimator_options['max_iterations']+1)

# plot log-likelihood
plt.plot(x, [it_data['current_log_likelihood'] for it_data in iteration_status_dictionaries], label='log_likelihood')
# plt.plot(x, [it_data['current_attachment'] for it_data in iteration_status_dictionaries], label='attachment')
# plt.plot(x, [it_data['current_regularity'] for it_data in iteration_status_dictionaries], label='regularity')

plt.xticks(x)

plt.style.use('default')
plt.legend()
plt.show()


#%%
## PLOT RESULTING TEMPLATES


####
#### LOAD RELEVANT INPUT DATA
####

import deformetrica as dfca

path_to_template__ini = template_specifications['skull']['filename']
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

# Initial template
ax = plt.subplot(gs[0, 0])
p = template_points__ini
c = template_connectivity__ini
ax.plot([p[c[:,0]][:,0], p[c[:,1]][:,0]], 
        [p[c[:,0]][:,1], p[c[:,1]][:,1]], 'k', linewidth=4)
ax.set_title('Initial template')

# Estimated template
ax = plt.subplot(gs[0, 1])
p = template_points__est
ax.plot([p[c[:,0]][:,0], p[c[:,1]][:,0]], [p[c[:,0]][:,1], p[c[:,1]][:,1]], 'k', linewidth=4)
ax.set_title('Estimated template')

# Estimated template and momenta
ax = plt.subplot(gs[0, 2])
x = control_points__est
ax.plot([p[c[:,0]][:,0], p[c[:,1]][:,0]], [p[c[:,0]][:,1], p[c[:,1]][:,1]], 'k', linewidth=4)
cmap = cm.get_cmap('tab10')
for i, m in enumerate(momenta__est):
    color = cmap(i % 10)[:3]
    ax.quiver(x[:,0], x[:,1], m[:,0], m[:,1], color=color, width=0.01, scale=75)
ax.set_title('Estimated template and momenta')

####
#### PLOT RAW VERSUS RECONSTRUCTED DATA
####

import torch 

figsize = 3
f = plt.figure(figsize=(5*figsize, 1*figsize))
gs = gridspec.GridSpec(1, 5)

for i, momentum__est in enumerate(momenta__est): 
    ax = plt.subplot(gs[0, i])
    color = cmap(i % 10)[:3]
  
    # Load and plot raw target. 
    path_to_target__raw = dataset_specifications['dataset_filenames'][i][0]['skull']
    target_id = dataset_specifications['subject_ids'][i]
    target_points__raw, _, target_connectivity__raw = dfca.io.DeformableObjectReader.read_file(path_to_target__raw, extract_connectivity=True)

    p = target_points__raw
    c = target_connectivity__raw
    ax.plot([p[c[:,0]][:,0], p[c[:,1]][:,0]], [p[c[:,0]][:,1], p[c[:,1]][:,1]], 'k', linewidth=2)
    ax.set_title(target_id)
  
    # Compute and plot the reconstruction of the target. 
    model.exponential.set_initial_momenta(torch.from_numpy(momentum__est).to(torch.float32))
    model.exponential.update()
    target_points__rec = model.exponential.get_template_points()['landmark_points'].detach().cpu().numpy()
  
    p = target_points__rec
    c = template_connectivity__ini
    ax.plot([p[c[:,0]][:,0], p[c[:,1]][:,0]], [p[c[:,0]][:,1], p[c[:,1]][:,1]], color=color, linewidth=2)

plt.style.use('default')
plt.show()


