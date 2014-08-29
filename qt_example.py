#!/usr/bin/python

import cv2
import sys, time
from PyQt4 import QtCore, QtGui
from qt_example_ui import Ui_Display
import ueye
import IS

class Display(QtGui.QMainWindow):
    """ This is the main Thread 
    Starts the other threads (eye tracking, video capture/recording)
    """
    enabled = True
    fc = 0
    last_t = time.time()
    def __init__(self, fps, parent=None):
        self.fps = 29
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Display()
        self.ui.setupUi(self)

        # add the guys we need for displaying frames 
        self.ui.scene = QtGui.QGraphicsScene(self.ui.layout)
        self.ui.view = QtGui.QGraphicsView(self.ui.scene)
        self.ui.layout.addWidget(self.ui.view)
        self.ui.image = QtGui.QGraphicsPixmapItem()
        self.ui.scene.addItem(self.ui.image)
        self.ui.view.centerOn(self.ui.image)

        self.vcr = VideoRecorder(fps)
        self.vcr.plug_in(self)
        self.vcr.start()

        self.connect( self.vcr, QtCore.SIGNAL("update(QString)"), self.update )

    def update(self):
        """ update display with frame from eye tracker """
        frame = self.vcr.frame
        height, width = frame.shape
        im = QtGui.QImage(frame.flatten(), width, height, QtGui.QImage.Format_Indexed8)
        pix = QtGui.QPixmap.fromImage(im)
        self.ui.image.setPixmap(pix)
        
    def closeEvent(self, event):
        self.vcr.close()

class VideoRecorder(QtCore.QThread):
    """ capture video and record to file """
    device = 'TL'
    fps = 60
    fc = 0 # this one gets reset every couple of seconds
    cfc = 0
    last_t = time.time()
    def __init__(self, fps):
        QtCore.QThread.__init__(self)
        self.keep_running = True
        self.fps = float(fps)
        self.configure_camera()
        self.fc = 0 # frame counter
        self.recording = False
        if self.camera.isOpened() == False:
            print "Something wrong, can't access camera"
            exit

    def plug_in(self, dp):
        """ make VCR aware of ET and display """
        self.dp = dp


    def configure_camera(self):
        if self.device == 'TL':
            print "using Thorlabs camera"
            self.camera = ueye.camera(1)
            self.camera.AllocImageMem(width=1280,height=1024,bitpixel=8)
            self.camera.SetImageMem()
            self.camera.SetAOI(x=0, y=0, width=640, height=480)
            print self.camera.GetAOI()        
            self.camera.SetFrameRate(self.fps)
            print "framerate: %s " % self.camera.GetFrameRate()
            self.camera.SetColorMode()
            self.camera.CaptureVideo()
        else:
            self.camera = cv2.VideoCapture(0)
            self.camera.set(cv2.cv.CV_CAP_PROP_FPS, self.fps)

    def get_frame(self):
        ret, self.frame = self.camera.read()
        try:
            height, width = self.frame.shape
        except:
            self.frame = cv2.cvtColor( self.frame, cv2.COLOR_RGB2GRAY )
            
    def run(self):
        """ main worker 
        get frame, share it with ET, Display, and write to file if desired """
        while True:
            self.get_frame()
            self.emit(QtCore.SIGNAL('update(QString)'), "update display" )
            time.sleep(1.0/self.fps)



    def close(self):
        if self.device == 'TL':
            self.camera.StopLiveVideo()
            self.camera.FreeImageMem()
            self.camera.ExitCamera()
        else:
            self.camera.release()
            self.out.release()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Please provide desired frame rate for the camera"
        print "Example: \"python " + sys.argv[0] + " 60\""
        sys.exit()
    app = QtGui.QApplication(sys.argv)
    dp = Display(sys.argv[1])
    dp.show()
    sys.exit(app.exec_())
