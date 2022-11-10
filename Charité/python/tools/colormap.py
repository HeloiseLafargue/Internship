import os
import deformetrica as dfca
from deformetrica.in_out.deformable_object_reader import DeformableObjectReader
import numpy as np
#from landmarkscalar import LandmarkScalar

obj = 'LV'
path_name = os.path.abspath('/home/icm-admin/Documents/Internship/data/TimeSeries_LV/output')
output_dir = os.path.join(path_name,'colormaps')

flag_all=1
number_of_time_points=100

expected = [None] * number_of_time_points
expected_dimension = [None] * number_of_time_points
expected_connectivity = [None] * number_of_time_points


# browse the files
age = 0
ind = -1
for k in range(0, number_of_time_points):
    ind = ind + 1
    if k % 10 == 0:
        age = age + 1
        ind = 0
        
        prefix = ('GeodesicRegression__GeodesicFlow__%s__tp_%s__age_%s.%s0' % (obj,k,age,ind))
        expected[k], expected_dimension[k], expected_connectivity[k] = DeformableObjectReader.read_file(
               os.path.join(path_name, prefix + '.vtk'), extract_connectivity=True)

os.makedirs(output_dir, exist_ok=True)

surface = dfca.core.observations.deformable_objects.landmarks.landmark
surface.points = expected[0]
surface.connectivity = expected_connectivity[0]
surface.scalars = np.zeros(len(surface.points))


if flag_all:
    #surface.write(output_dir, prefix + '%d.vtk' % 0)
    
    connec_names = {2: 'LINES', 3: 'POLYGONS'}


    with open(os.path.join(output_dir, prefix + '%d.vtk' % 0), 'w', encoding='utf-8') as f:
        s = '# vtk DataFile Version 3.0\nvtk output\nASCII\nDATASET POLYDATA\nPOINTS ' \
                '{} float\n'.format(len(surface.points))
        f.write(s)

        for p in surface.points:
                str_p = [str(elt) for elt in p]
                if len(p) == 2:
                    str_p.append(str(0.))
                s = ' '.join(str_p) + '\n'
                f.write(s)

        if surface.connectivity is not None:
                a, connec_degree = surface.connectivity.shape
                s = connec_names[connec_degree] + ' {} {}\n'.format(a, a * (connec_degree+1))
                f.write(s)
                for face in surface.connectivity:
                    s = str(connec_degree) + ' ' + ' '.join([str(elt) for elt in face]) + '\n'
                    f.write(s)

        if surface.scalars is not None:
                a, connec_degree = surface.connectivity.shape
                s = 'CELL_DATA %d \nPOINT_DATA %d\nSCALARS scalars double\nLOOKUP_TABLE default\n' % (a,
                                                          len(surface.points))
                f.write(s)
                for scalar in surface.scalars:
                    s = '%f' % scalar + '\n'
                    f.write(s)
        f.close()


d = 0

for k in range(1, number_of_time_points):
    surface = dfca.core.observations.deformable_objects.landmarks.landmark
    # surface = LandmarkScalar()
    surface.points = expected[k]
    surface.connectivity = expected_connectivity[k]
    d = d +1# np.sqrt(np.sum((expected[k]-expected[k-1]) ** 2, axis=1))
    surface.scalars = d
    if flag_all:
        #surface.write(path_name / 'colormaps', prefix + '%d.vtk' % k)
        connec_names = {2: 'LINES', 3: 'POLYGONS'}


        with open(os.path.join(output_dir, prefix + '%d.vtk' % k), 'w', encoding='utf-8') as f:
            s = '# vtk DataFile Version 3.0\nvtk output\nASCII\nDATASET POLYDATA\nPOINTS ' \
                    '{} float\n'.format(len(surface.points))
            f.write(s)

            for p in surface.points:
                    str_p = [str(elt) for elt in p]
                    if len(p) == 2:
                        str_p.append(str(0.))
                    s = ' '.join(str_p) + '\n'
                    f.write(s)

            if surface.connectivity is not None:
                    a, connec_degree = surface.connectivity.shape
                    s = connec_names[connec_degree] + ' {} {}\n'.format(a, a * (connec_degree+1))
                    f.write(s)
                    for face in surface.connectivity:
                        s = str(connec_degree) + ' ' + ' '.join([str(elt) for elt in face]) + '\n'
                        f.write(s)

            if surface.scalars is not None:
                    a, connec_degree = surface.connectivity.shape
                    s = 'CELL_DATA %d \nPOINT_DATA %d\nSCALARS scalars double\nLOOKUP_TABLE default\n' % (a,
                                                              len(surface.points))
                    f.write(s)
                    for scalar in surface.scalars:
                        s = '%f' % scalar + '\n'
                        f.write(s)
            f.close()
    else:
        if k == number_of_time_points-1:
            #surface.write(path_name / 'colormaps', prefix + '%d.vtk' % k)
            connec_names = {2: 'LINES', 3: 'POLYGONS'}


            with open(os.path.join(output_dir, prefix + '%d.vtk' % k), 'w', encoding='utf-8') as f:
                s = '# vtk DataFile Version 3.0\nvtk output\nASCII\nDATASET POLYDATA\nPOINTS ' \
                        '{} float\n'.format(len(surface.points))
                f.write(s)

                for p in surface.points:
                        str_p = [str(elt) for elt in p]
                        if len(p) == 2:
                            str_p.append(str(0.))
                        s = ' '.join(str_p) + '\n'
                        f.write(s)

                if surface.connectivity is not None:
                        a, connec_degree = surface.connectivity.shape
                        s = connec_names[connec_degree] + ' {} {}\n'.format(a, a * (connec_degree+1))
                        f.write(s)
                        for face in surface.connectivity:
                            s = str(connec_degree) + ' ' + ' '.join([str(elt) for elt in face]) + '\n'
                            f.write(s)

                if surface.scalars is not None:
                        a, connec_degree = surface.connectivity.shape
                        s = 'CELL_DATA %d \nPOINT_DATA %d\nSCALARS scalars double\nLOOKUP_TABLE default\n' % (a,
                                                                  len(surface.points))
                        f.write(s)
                        for scalar in surface.scalars:
                            s = '%f' % scalar + '\n'
                            f.write(s)
                f.close()