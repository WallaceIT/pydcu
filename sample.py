import ueye
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import ctypes


camera = ueye.camera(1)
camera.AllocImageMem(width=1280,height=1024,bitpixel=8)
camera.SetImageMem()
camera.SetImageSize()
camera.FreezeVideo()
camera.CopyImageMem()
im = plt.imshow(camera.data, cmap=cm.gray, aspect='equal')
plt.show()
camera.FreeImageMem()
camera.ExitCamera()
