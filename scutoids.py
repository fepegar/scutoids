from math import tau
import numpy as np
import vtk

tau = 2*np.pi

points_hexagon = []

def get_polygon_points(N, z, radius=1):
    points = []
    for i in range(N):
        theta = i / float(N) * tau
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        points.append(np.array([x, y, z]))
    return points


def to_points_dict(points):
    return {i: point for (i, point) in enumerate(points)}


def to_vtk_list(iterable):
    vtkIdList = vtk.vtkIdList()
    for i in iterable:
        vtkIdList.InsertNextId(i)
    return vtkIdList


radius = 12
z = 20

points_hexagon = get_polygon_points(6, -z, radius)
points_pentagon = get_polygon_points(5, z, radius)
point_middle = np.array([-radius * 1.2, 0, 0])

points_list = points_hexagon + points_pentagon
points_list.append(point_middle)

points = vtk.vtkPoints()
cells = vtk.vtkCellArray()

for point in points_list:
    print(points.InsertNextPoint(point))

faces = (
    (0, 1, 2, 3, 4, 5),
    (6, 7, 8, 9, 10),
    (0, 1, 7, 6),
    (1, 2, 8, 7),
    (2, 3, 11, 8),
    (3, 4, 9, 11),
    (4, 5, 10, 9),
    (0, 5, 10, 6),
    (8, 9, 11),
)

for face in faces:
    cells.InsertNextCell(to_vtk_list(face))


polyData = vtk.vtkPolyData()
polyData.SetPoints(points)
polyData.SetPolys(cells)

modelNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLModelNode')
modelNode.CreateDefaultDisplayNodes()
modelNode.SetAndObservePolyData(polyData)

displayNode = modelNode.GetDisplayNode()
displayNode.SetColor(0.8, 0, 0)
displayNode.SetRepresentation(slicer.vtkMRMLModelDisplayNode.WireframeRepresentation)
displayNode.SetLineWidth(5)
