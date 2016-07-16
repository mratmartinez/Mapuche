from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSignal, pyqtSlot

class openMapWindow(QtGui.QWidget):
    def __init__(self):
        super(openMapWindow,self).__init__()
        uic.loadUi('UI/openMap.ui', self)
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.open)
    
    @pyqtSlot()
    def open(self):
        print("Test1")
