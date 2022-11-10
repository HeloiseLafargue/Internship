#ICP

#%%

"Try ICP method"
import os
import vtk

data_path = os.path.abspath('/home/icm-admin/Documents/Internship/data/test_icp/')
data_base = os.path.join(data_path, 'data/')

def applyICP(source, target):

    icp = vtk.vtkIterativeClosestPointTransform()
    icp.SetSource(source)
    icp.SetTarget(target)
    icp.GetLandmarkTransform().SetModeToRigidBody()
    icp.Update()
    t = vtk.vtkTransform()
    t.SetMatrix(icp.GetMatrix())
    return t 

source = os.path.join(data_base, 'Subject01_LA_elongated_PV.vtk')
target = os.path.join(data_base, 'Subject01_LA_elongated_PV.vtk')

applyICP(source, target)




#%%
import vtk
from vtk import *
#import hybrid
#from hybrid import *

# ============ create source points ==============
print ("Creating source points...")
sourcePoints = vtk.vtkPoints()
sourceVertices = vtk.vtkCellArray()

id = sourcePoints.InsertNextPoint(1.0, 0.1, 0.0)
sourceVertices.InsertNextCell(1)
sourceVertices.InsertCellPoint(id)

id = sourcePoints.InsertNextPoint(0.1, 1.1, 0.0)
sourceVertices.InsertNextCell(1)
sourceVertices.InsertCellPoint(id)

id = sourcePoints.InsertNextPoint(0.0, 0.1, 1.0)
sourceVertices.InsertNextCell(1)
sourceVertices.InsertCellPoint(id)

source = vtk.vtkPolyData()
source.SetPoints(sourcePoints)
source.SetVerts(sourceVertices)
#source.Update()

print ("Displaying source points...")
# ============ display source points ==============
pointCount = 3
index = 0
while index < pointCount:
    point = [0,0,0]
    sourcePoints.GetPoint(index, point)
    print ("source point[%s]=%s") # (index,point)
    index += 1

#============ create target points ==============
print ("Creating target points...")
targetPoints = vtk.vtkPoints()
targetVertices = vtk.vtkCellArray()

id = targetPoints.InsertNextPoint(1.0, 0.0, 0.0)
targetVertices.InsertNextCell(1)
targetVertices.InsertCellPoint(id)

id = targetPoints.InsertNextPoint(0.0, 1.0, 0.0)##
targetVertices.InsertNextCell(1)
targetVertices.InsertCellPoint(id)

id = targetPoints.InsertNextPoint(0.0, 0.0, 1.0)
targetVertices.InsertNextCell(1)
targetVertices.InsertCellPoint(id)

target = vtk.vtkPolyData()
target.SetPoints(targetPoints)
target.SetVerts(targetVertices)
target.Update()

# ============ display target points ==============
print ("Displaying target points...")
pointCount = 3
index = 0
while index < pointCount:
    point = [0,0,0]
    targetPoints.GetPoint(index, point)
    print ("target point[%s]=%s") #(index,point)
    index += 1

print ("Running ICP ----------------")
# ============ run ICP ==============
icp = vtk.vtkIterativeClosestPointTransform()
icp.SetSource(source)
icp.SetTarget(target)
icp.GetLandmarkTransform().SetModeToRigidBody()
#icp.DebugOn()
icp.SetMaximumNumberOfIterations(20)
icp.StartByMatchingCentroidsOn()
icp.Modified()
icp.Update()

icpTransformFilter = vtk.vtkTransformPolyDataFilter()
icpTransformFilter.SetInputData(source)
icpTransformFilter.SetTransform(icp)
icpTransformFilter.Update()

transformedSource = icpTransformFilter.GetOutput()

# ============ display transformed points ==============
pointCount = 3
index = 0
while index < pointCount:
    point = [0,0,0]
    transformedSource.GetPoint(index, point)
    print ("xformed source point[%s]=%s") #% (index,point)
    index += 1

#%%
import os
import open3d as o3d
import numpy as np
import copy

data_path = '/home/icm-admin/Documents/Internship/data/test/'
data_base = os.path.join(data_path, 'data/')

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp],
                                      zoom=0.4459,
                                      front=[0.9288, -0.2951, -0.2242],
                                      lookat=[1.6784, 2.0612, 1.4451],
                                      up=[-0.3402, -0.9189, -0.1996])
    

source = o3d.io.read_triangle_mesh(os.path.join(data_base, 'Subject01_LA_raw_moved.vtk'))
target = o3d.io.read_triangle_mesh(os.path.join(data_base, 'LA_Sphere_scaled075.vtk'))
threshold = 0.02
trans_init = np.asarray([[0.862, 0.011, -0.507, 0.5],
                          [-0.139, 0.967, -0.215, 0.7],
                          [0.487, 0.255, 0.835, -1.4], [0.0, 0.0, 0.0, 1.0]])
draw_registration_result(source, target, trans_init)

# print("Initial alignment")
# evaluation = o3d.pipelines.registration.evaluate_registration(
#     source, target, threshold, trans_init)
# print(evaluation)


# print("Apply point-to-point ICP")
# reg_p2p = o3d.pipelines.registration.registration_icp(
#     source, target, threshold, trans_init,
#     o3d.pipelines.registration.TransformationEstimationPointToPoint())
# print(reg_p2p)
# print("Transformation is:")
# print(reg_p2p.transformation)
# draw_registration_result(source, target, reg_p2p.transformation)

# reg_p2p = o3d.pipelines.registration.registration_icp(
#     source, target, threshold, trans_init,
#     o3d.pipelines.registration.TransformationEstimationPointToPoint(),
#     o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=2000))
# print(reg_p2p)
# print("Transformation is:")
# print(reg_p2p.transformation)
# draw_registration_result(source, target, reg_p2p.transformation)
