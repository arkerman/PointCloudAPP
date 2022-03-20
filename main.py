#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :  main.py
# @Time      :  2022/3/19 13:21
# @Author    :  Liu
# @Software  :  PyCharm

import vtk
from PyQt5 import QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PointCloud_APP import Ui_MainWindow
import open3d as o3d
import numpy as np
from vtk.util.numpy_support import numpy_to_vtk


class Mywindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(Mywindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('PointCloud_APP')
        # A button click event, the response function is: read_file_vis
        self.pushButton.clicked.connect(self.read_file_vis)
        self.frame = QtWidgets.QFrame()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.formLayout.addWidget(self.vtkWidget)
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.show()
        self.iren.Initialize()

    def read_file_vis(self):

        filepath, filetype = QtWidgets.QFileDialog.getOpenFileName(self, 'openfile', '../../PCD_File',
                                                                   'pcd files (*.pcd *.ply)')
        self.lineEdit.setText(filepath)
        # Read point cloud file
        pcd = o3d.io.read_point_cloud(filepath)
        source_data = np.asarray(pcd.points)
        points = vtk.vtkPoints()
        # Convert numpy array to VTK data
        points.SetData(numpy_to_vtk(source_data))
        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)
        vertex = vtk.vtkVertexGlyphFilter()
        vertex.SetInputData(polydata)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(vertex.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        # Point cloud color normalization
        actor.GetProperty().SetColor(1, 1, 1)
        self.ren.SetBackground(0, 0, 0)
        self.ren.AddActor(actor)
        self.ren.ResetCamera()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Mywindow()
    window.show()
    sys.exit(app.exec_())
