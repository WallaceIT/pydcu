import ueye
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import ctypes


camera = ueye.camera(1)
camera.AllocImageMem(width=1024, height=768, bitpixel=8)
camera.SetImageMem()
#camera.SetImageSize(x=1280, y=1024)
#camera.SetImagePos()
#print(camera.SetAOI(x=0, y=0, width=1024, height=768))
# print(camera.GetImageSize())
camera.SetColorMode()
camera.FreezeVideo()
camera.CopyImageMem()
im = plt.imshow(camera.data, cmap=cm.gray, aspect='equal')
plt.show()
camera.FreeImageMem()
camera.ExitCamera()
