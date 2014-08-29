from PyQt4 import QtGui, QtCore
import gobject, sys
import ueye
import numpy as np
import ctypes

class Viewer(QtGui.QMainWindow):
    def __init__(self, *args):
        super(Viewer, self).__init__(*args)
        self.width = 1280
        self.height = 1024
        self.setup_graphics_view()
        self.setup_camera()

    def setup_graphics_view(self):
        self.graphics = QtGui.QGraphicsView()
        self.setCentralWidget(self.graphics)
        self.scene = QtGui.QGraphicsScene()
        self.graphics.setScene(self.scene)
        self.pixmap = QtGui.QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap)
        self.graphics.centerOn(self.pixmap)


    def setup_camera(self):
        self.camera = ueye.camera(1)
        self.camera.AllocImageMem(self.width, self.height, bitpixel=8)
        self.camera.SetImageMem()
        self.camera.SetImageSize()
        self.camera.SetColorMode()
        self.camera.CaptureVideo()
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.update_image)
        self.timer.start(1000)
        
    def update_image(self):
        if hasattr(self,"camera_pixmap"):
            self.scene.removeItem(self.camera_pixmap)
        self.camera.CopyImageMem()
        im = QtGui.QImage(self.camera.data.flatten(), self.width, self.height, QtGui.QImage.Format_Indexed8)#Format_RGB888)
        pix = QtGui.QPixmap.fromImage(im)
        self.pixmap.setPixmap(pix)
        self.timer.start(100)

    def closeEvent(self, event):
        self.camera.StopLiveVideo()
        self.camera.FreeImageMem()
        self.camera.ExitCamera()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main_window = Viewer()
    main_window.show()
    app.exec_()
