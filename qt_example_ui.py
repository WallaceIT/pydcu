# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_example.ui'
#
# Created: Thu Sep  4 15:48:33 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Display(object):
    def setupUi(self, Display):
        Display.setObjectName(_fromUtf8("Display"))
        Display.resize(1300, 1052)
        Display.setAccessibleName(_fromUtf8(""))
        Display.setAnimated(True)
        self.widget = QtGui.QWidget(Display)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.widget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 1291, 981))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.layout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.layout.setMargin(0)
        self.layout.setObjectName(_fromUtf8("layout"))
        Display.setCentralWidget(self.widget)
        self.menubar = QtGui.QMenuBar(Display)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        Display.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Display)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Display.setStatusBar(self.statusbar)

        self.retranslateUi(Display)
        QtCore.QMetaObject.connectSlotsByName(Display)

    def retranslateUi(self, Display):
        Display.setWindowTitle(_translate("Display", "Display", None))

