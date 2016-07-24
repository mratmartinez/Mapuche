from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class openMapWindow(QtWidgets.QDialog):
    def __init__(self):
        super(openMapWindow,self).__init__()
        uic.loadUi('UI/openMap.ui', self)
        self.buttonBox.accepted.connect(self.open)
    
    @pyqtSlot()
    def open(self):
        print("Test1")
