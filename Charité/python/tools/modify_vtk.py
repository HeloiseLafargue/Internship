# trace generated using paraview version 5.10.0-RC1
import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 10

#### import the simple module from the paraview
from paraview.simple import *

# get active source.
subject02_LA_elongated_PVvtk = GetActiveSource()
subject02_LA_elongated_PVvtkDisplay = GetDisplayProperties(subject02_LA_elongated_PVvtk, view=renderView1)

subject02_LA_elongated_PVvtkDisplay.Orientation = [0.0, 20.0, 0.0]
subject02_LA_elongated_PVvtkDisplay.PolarAxes.Translation = [0.0, 0.0, 4.0]




#%%


import os
import vtk

data_path = os.path.abspath('/home/icm-admin/Documents/Internship/data/test_vtk/')
data_base = os.path.join(data_path, 'data/')
vtk_file = os.path.join(data_base, 'LA_Sphere.vtk')

# reader = vtk.vtkXMLImageDataReader()
# reader.SetFileName('result')
# reader.Update()


transform = vtk.vtkTransform()
transform.RotateX(1)
transform.RotateY(1)
transform.RotateZ(2)
transform.Translate(0, 1, 2)

