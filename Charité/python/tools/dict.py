## IMPORT AND RUN DEFORMETRICA

import os
import deformetrica as dfca

data_path = '/home/icm-admin/Documents/Internship/data/examples/examples/'
data_base = os.path.join(data_path, 'registration/landmark/3d/bundles_cortico/data/')

iteration_status_dictionaries = []

def estimator_callback(status_dict):
    iteration_status_dictionaries.append(status_dict)
    return True

# using python dictionnaries, transcription of the xml file
# set the data, model, parameters: transcription of the xml files into dictionnaries
dataset_specifications = {
    'dataset_filenames': [
        [{'bundle': os.path.join(data_base, 'subject_bundle.vtk'),
        'putamen': os.path.join(data_base, 'subject_putamen.vtk')}]],
    'subject_ids': ['subj1']
}

template_specifications = {
    'bundle': {'deformable_object_type': 'polyline',
              'kernel_type': 'keops', 'kernel_width': 11,
              'noise_std': 1.0,
              'filename': os.path.join(data_base, 'bundle_prototype.vtk'),
              'attachment_type': 'varifold'},
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

