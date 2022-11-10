import os
import deformetrica as dfca

# geodesic regression
data_path = '/home/icm-admin/Documents/Internship/data/examples/examples/regression/image/2d/cross/'

arg = dfca.io.XmlParameters() # creation of the XmlParameters object

model_path =os.path.join(data_path, 'model.xml')
dataset_path =os.path.join(data_path, 'data_set.xml')
opt_param_path =os.path.join(data_path, 'optimization_parameters.xml')

arg.read_all_xmls(model_path, dataset_path, opt_param_path) # reading of the 3 xml files

template_specifications_xml = arg.template_specifications # access to the model dictionnarie of arg
dataset_specifications_xml = dfca.io.get_dataset_specifications(arg) # same for data
estimator_options_xml = dfca.io.get_estimator_options(arg) # same for estimator