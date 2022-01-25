from vtk.util.vtkImageImportFromArray import *
import vtk

class KeyPressInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
     
    def __init__(self,parent=None):
        self.parent = vtk.vtkRenderWindowInteractor()
        if(parent is not None):
            self.parent = parent
 
        self.AddObserver("KeyPressEvent",self.keyPress)
 
    def keyPress(self,obj,event):
        key = self.parent.GetKeySym()
        if key == 'Up':
            
            gradtfun.AddPoint(-100, 1.0)
            gradtfun.AddPoint(10, 1.0)
            gradtfun.AddPoint(20, 1.0)
            
            volumeProperty.SetGradientOpacity(gradtfun)
            #下面这一行是关键，实现了actor的更新
            renWin.Render()
        if key == 'Down':
            
            
            tfun.AddPoint(1129, 0)
            tfun.AddPoint(1300.0, 0.1)
            tfun.AddPoint(1600.0, 0.2)
            tfun.AddPoint(2000.0, 0.1)
            tfun.AddPoint(2200.0, 0.1)
            tfun.AddPoint(2500.0, 0.1)
            tfun.AddPoint(2800.0, 0.1)
            tfun.AddPoint(3000.0, 0.1)
            #下面这一行是关键，实现了actor的更新
            renWin.Render()
    

def StartInteraction():
    renWin.SetDesiredUpdateRate(10)

def EndInteraction():
    renWin.SetDesiredUpdateRate(0.001)

def ClipVolumeRender(obj):
    obj.GetPlanes(planes)
    volumeMapper.SetClippingPlanes(planes)