from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSignal, pyqtSlot
import opnMap, newMap
import pytes, sys

class MainWindow(QtGui.QDialog):
    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi('UI/Main.ui', self)
        self.opnMp = opnMap.openMapWindow()
        self.newMp = newMap.newMapWindow()
        self.connect(self.opnMapbtn, QtCore.SIGNAL("clicked()"), self.openMap)
        self.connect(self.newMapbtn, QtCore.SIGNAL("clicked()"), self.newMap)
    
    @pyqtSlot()
    def openMap(self):
        self.opnMp.show()
    
    def newMap(self):
        self.newMp.show()
        
def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
