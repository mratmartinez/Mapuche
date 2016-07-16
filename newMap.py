from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSignal, pyqtSlot
from Pytes import pytes
import sys

class newMapWindow(QtGui.QWidget):
    def __init__(self):
        super(newMapWindow,self).__init__()
        uic.loadUi('UI/newMap.ui', self)
        self.connect(self.saveBox, QtCore.SIGNAL("accepted()"), self.save)
        self.connect(self.saveBox, QtCore.SIGNAL("rejected()"), self.cancel)
        self.items = ["Mapache v1"]
        for i in self.items:
            self.listWidget.addItem(i)
    
    def writefile(self):
        file = open(self.archivo, "w")
        self.header = self.formats + str(self.layer) + str(self.tiles) + " "
        file.write(self.header)
        file.close()
        file = pytes.Pyte(self.archivo)
        for l in range(self.layer):
            file.op.read()
            for i in range((self.tiles*(10**self.counter))**2):
                file.write(0b00000000)
        file.stapit()
        self.close()
        
    
    @pyqtSlot()
    def save(self):
        if self.listWidget.currentItem().text() == "Mapache v1":
            self.formats = "MA1"
        self.layer = self.horizontalSlider.value()
        self.counter = 0
        try:
            self.tiles = int(self.sizeEdit.text())
        except:
            QtGui.QMessageBox.about(self, 'Error','Size can only be a number')
            return
        if self.nameEdit.text() == "":
            QtGui.QMessageBox.about(self, 'Error','You didn\'t wrote a name to your file!')
        else:
            while len(str(self.tiles))>1:
                self.tiles = int(self.tiles/10)
                self.counter += 1
            self.archivo = self.nameEdit.text() + "." + self.formats.lower()
            self.writefile()

    def cancel(self):
        self.close()
