from PyQt5.QtWidgets import QFrame,QVBoxLayout
from numpy import min,max
from SimpleITK import ReadImage
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.util import numpy_support
from vtkmodules.all import vtkBoxWidget,vtkPolyDataMapper,vtkOutlineFilter,vtkImageData,VTK_UNSIGNED_CHAR,vtkRenderer,vtkImageShiftScale,vtkPiecewiseFunction,vtkColorTransferFunction,vtkGPUVolumeRayCastMapper,vtkVolumeProperty,vtkVolume
from copy import deepcopy




def model(fp, Myslices,flag,label):
        slices = deepcopy(Myslices)
        if(label):
            slices_only = deepcopy(Myslices)
            slices_only[slices_only==0] = 0
            slices_only[slices_only==184] = 2
            slices_only[slices_only==220] = 1
            flag=True
        else:
            slices_only = deepcopy(Myslices)
            slices_only[slices_only < 254] = 0
            slices_only[slices_only == 254] = 1
            slices_only[slices_only == 255] = 2
        slices[slices==254]=235
        #加上预制色
        slices[1,1,1] = 255
        slices[1,1,2]=235
        slices_only[1,1,1] = 1
        slices_only[1, 1, 2] = 2
        #加入VTK体绘制窗口
        #直接加入窗口
        ds = ReadImage(fp[0])
        #data = sitk.GetArrayFromImage(ds)
        if (flag == True):
            slices=deepcopy(slices_only)
            del slices_only
        data=slices
        #print(type(slices))
        #print("slices",slices.shape)
        spacing = ds.GetSpacing()               #三维数据的间隔
        #print('spacing_of_data',spacing)
        # data = data[50:]
        # data = data[:,:,300:]
        srange = [min(data),max(data)]
        #print('shape_of_data_chenged',data.shape)
        #img_arr = vtkImageImportFromArray()        #创建一个空的vtk类-----vtkImageImportFromArray
        #print('img_arr: ',img_arr)
        #try:
            #img_arr.SetArray(data)#把array_data塞到vtkImageImportFromArray（array_data）
            #print(img_arr)
        #except:
            #print("I AM A ERROR")
        #img_arr.SetDataSpacing(spacing)                   #设置spacing
        origin = (0,0,0)
        #img_arr.SetDataOrigin(origin)                     #设置vtk数据的坐标系原点
        #img_arr.Update()
        #print(img_arr.GetOutput())
        vtk_data = numpy_support.numpy_to_vtk(slices.ravel(), array_type=VTK_UNSIGNED_CHAR)
        img_array=vtkImageData()
        img_array.SetDimensions((512,512,slices.shape[0]))
        # img_array.SetSpacing(spacing)
        img_array.SetSpacing(1,1,2)
        img_array.SetOrigin(origin)
        img_array.GetPointData().SetScalars(vtk_data)
        frame = QFrame()
        #frame.setGeometry(360,780,480,480)
        frame.setFrameShape(QFrame.Box)
        v1=QVBoxLayout()
        vtkWidget = QVTKRenderWindowInteractor()
        v1.addWidget(vtkWidget)
        frame.setLayout(v1)
        #self.vl.addWidget(self.vtkWidget)
        ren = vtkRenderer()
        renWin=vtkWidget.GetRenderWindow()
        vtkWidget.GetRenderWindow().AddRenderer(ren)
        iren = vtkWidget.GetRenderWindow().GetInteractor()
        Min = srange[0]
        Max = srange[1]
        diff = Max - Min             #体数据极差
        inter = 4200 / diff
        shift = -Min
        shifter = vtkImageShiftScale()  # 对偏移和比例参数来对图像数据进行操作 数据转换，之后直接调用shifter
        shifter.SetShift(shift)
        shifter.SetScale(inter)
        shifter.SetOutputScalarTypeToUnsignedShort()
        #shifter.SetInputData(img_array.GetOutput())
        try:
            shifter.SetInputData(img_array)
        except:
            print("Error1")
        shifter.ReleaseDataFlagOff()
        shifter.Update()
        try:
            tfun = vtkPiecewiseFunction()  # 不透明度传输函数---放在tfun
            tfun.AddPoint(1129, 0)
            tfun.AddPoint(1300.0, 0.1)
            tfun.AddPoint(1600.0, 0.12)
            tfun.AddPoint(2000.0, 0.13)
            tfun.AddPoint(2200.0, 0.14)
            tfun.AddPoint(2500.0, 0.16)
            tfun.AddPoint(2800.0, 0.17)
            tfun.AddPoint(3000.0, 0.18)
        except:
            print("Error3")
        try:
            gradtfun = vtkPiecewiseFunction()  # 梯度不透明度函数---放在gradtfun
            gradtfun.AddPoint(-1000, 9)
            gradtfun.AddPoint(0.5, 9.9)
            gradtfun.AddPoint(1, 10)
        except:
            print("Error4")
        ctfun = vtkColorTransferFunction()  # 颜色传输函数---放在ctfun
        # if len(slices[slices > 3]) > 0:
        if flag==False:
            ctfun.AddRGBPoint(0.0, 0.5, 0.0, 0.0)
            ctfun.AddRGBPoint(600.0, 139 / 255, 134 / 255, 130 / 255)
            ctfun.AddRGBPoint(1280.0, 139 / 255, 134 / 255, 130 / 255)
            ctfun.AddRGBPoint(1960.0, 139 / 255, 134 / 255, 130 / 255)
            ctfun.AddRGBPoint(2800.0, 139 / 255, 134 / 255, 130 / 255)
            ctfun.AddRGBPoint(3700.0,  139 / 255, 134 / 255, 139 / 255)
            ctfun.AddRGBPoint(3900.0, 0 / 255, 255 / 255, 0 / 255)
            ctfun.AddRGBPoint(4020.0, 0 / 255, 255 / 255, 0 / 255)
            ctfun.AddRGBPoint(4050.0, 255 / 255, 0 / 255, 0 / 255)
            ctfun.AddRGBPoint(4100.0, 255 / 255, 0 / 255, 0 / 255)
        else:
            ctfun.AddRGBPoint(0.0, 0, 0.0, 0.0)
            ctfun.AddRGBPoint(1500, 0 , 0, 0)
            ctfun.AddRGBPoint(2000.0, 0, 255 / 255, 0)
            ctfun.AddRGBPoint(2500.0, 0, 255 / 255, 0)
            ctfun.AddRGBPoint(2700.0, 255 / 255, 0 / 255, 0 / 255)
            ctfun.AddRGBPoint(3200.0, 255 / 255, 0 / 255, 0 / 255)
            ctfun.AddRGBPoint(4100.0, 255 / 255, 0 / 255, 0 / 255)
        try:
            volumeMapper = vtkGPUVolumeRayCastMapper()   #映射器volumnMapper使用vtk的管线投影算法
            volumeMapper.SetInputData(shifter.GetOutput())   #向映射器中输入数据：shifter(预处理之后的数据)
            volumeProperty = vtkVolumeProperty()         #创建vtk属性存放器,向属性存放器中存放颜色和透明度
            volumeProperty.SetColor(ctfun)  
            volumeProperty.SetScalarOpacity(tfun)
        # volumeProperty.SetGradientOpacity(gradtfun)
            volumeProperty.SetInterpolationTypeToLinear()    #???
            volumeProperty.ShadeOn() 
        except:
            print("Error6")           
        try:
            newvol = vtkVolume()                 #演员       
            newvol.SetMapper(volumeMapper)
            newvol.SetProperty(volumeProperty)
        except:
            print("Error2")
        try:
            outline = vtkOutlineFilter()
            outline.SetInputConnection(shifter.GetOutputPort())
        except:
            print("Error7")
        try:
            outlineMapper = vtkPolyDataMapper()
            outlineMapper.SetInputConnection(outline.GetOutputPort())
        except:
            print("Error8")
        #try:
            #outlineActor = vtk.vtkActor()
            #outlineActor.SetMapper(outlineMapper)
        #except:
            #print("Error9")
        try:
            #ren.AddActor(outlineActor)
            ren.AddVolume(newvol)
            ren.SetBackground(0, 0, 0)
            renWin.SetSize(480, 480)
        except:
            print("Error10")
        # planes = vtk.vtkPlanes()
        boxWidget = vtkBoxWidget()
        boxWidget.SetInteractor(iren)
        boxWidget.SetPlaceFactor(1.0)
        boxWidget.PlaceWidget(0,0,0,0,0,0)
        boxWidget.InsideOutOn()
        outlineProperty = boxWidget.GetOutlineProperty()
        outlineProperty.SetRepresentationToWireframe()
        outlineProperty.SetAmbient(1.0)
        outlineProperty.SetAmbientColor(1, 1, 1)
        outlineProperty.SetLineWidth(9)
        selectedOutlineProperty = boxWidget.GetSelectedOutlineProperty()
        selectedOutlineProperty.SetRepresentationToWireframe()
        selectedOutlineProperty.SetAmbient(1.0)
        selectedOutlineProperty.SetAmbientColor(1, 0, 0)
        selectedOutlineProperty.SetLineWidth(3)
        ren.ResetCamera()
        iren.Initialize()
        renWin.Render()
        iren.Start()
        return frame,vtkWidget




    