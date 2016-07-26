from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from Pytes import pytes
import opnMap, newMap, newtm, newProj
import sys

class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi('UI/Main.ui', self)
        self.opnMp = opnMap.openMapWindow()
        self.newMp = newMap.newMapWindow()
        self.newTm = newtm.newtmWindow()
        self.newProj = newProj.newProjWindow()
        self.opnMapbtn.clicked.connect(self.openMap)
        self.newMapbtn.clicked.connect(self.newMap)
        self.newTlmbtn.clicked.connect(self.newtilemap)
        self.newProjbtn.clicked.connect(self.newProjW)
    
    @pyqtSlot()
    def openMap(self):
        self.opnMp.show()
    
    def newMap(self):
        self.newMp.show()
        
    def newtilemap(self):
        self.newTm.show()
    
    def newProjW(self):
        self.newProj.show()
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
