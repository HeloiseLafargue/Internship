## IMPORT AND RUN DEFORMETRICA

import os
import deformetrica as dfca


path = os.path.abspath('/home/icm-admin/Documents/Internship/data/examples/examples/principal_geodesic_analysis/landmark/2D/starmen/')

iteration_status_dictionaries = []

def estimator_callback(status_dict):
    iteration_status_dictionaries.append(status_dict)
    return True

# Using XmlParameters
arg = dfca.io.XmlParameters() # creation of the XmlParameters object

model_path =os.path.join(path, 'model.xml')
dataset_path =os.path.join(path, 'data_set.xml')
opt_param_path =os.path.join(path, 'optimization_parameters.xml')

arg.read_all_xmls(model_path, dataset_path, opt_param_path) # reading of the 3 xml files

template_specifications_xml = arg.template_specifications # access to the model dictionnarie of arg
dataset_specifications_xml = dfca.io.get_dataset_specifications(arg) # same for data
estimator_options_xml = dfca.io.get_estimator_options(arg) # same for estimator

estimator_options_xml.update({'callback': estimator_callback})

# # instantiate a Deformetrica object
# deformetrica = dfca.Deformetrica(output_dir='output', verbosity='INFO')

# #perform a deterministic atlas estimation
# model = deformetrica.estimate_deterministic_atlas(template_specifications_xml, dataset_specifications_xml,
#                                                 estimator_options=estimator_options_xml,
#                                                   model_options={'deformation_kernel_type': 'keops', 'deformation_kernel_width': 15, 'dtype': 'float32'})

