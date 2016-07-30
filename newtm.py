from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PIL import Image
import os, tempfile

class TARWindow(QtWidgets.QDialog):
    def __init__(self, resource):
        super(TARWindow,self).__init__()
        uic.loadUi('UI/tartm.ui', self)
        self.tmp_dir = tempfile.mkdtemp()
        self.resource = Image.open(resource)
        self.h = self.resource.size[0]
        self.w = self.resource.size[1]
        for i in os.listdir(self.tmp_dir):
            if (i.lower().endswith('.png') or i.lower().endswith('.bmp')):
                self.resourceView.addItem(i)

class newtmWindow(QtWidgets.QDialog):
    def __init__(self):
        super(newtmWindow,self).__init__()
        uic.loadUi('UI/newtm.ui', self)
        self.refresh()
        self.chooseBtn.clicked.connect(self.pickfolder)
        self.saveBox.accepted.connect(self.save)
        self.saveBox.rejected.connect(self.cancel)
        self.horizontalSlider.valueChanged.connect(self.refresh)
        self.items = ["TAR TileMap"]
        for i in self.items:
            self.listWidget.addItem(i)

    def refreshdir(self):
        for i in os.listdir(self.directory):
            if (i.lower().endswith('.png') or i.lower().endswith('.bmp')):
                self.listFiles.addItem(i)

    def TARTilemap(self, resource):
        self.tarfile = TARWindow(resource)
        self.tarfile.show()
        #FIX THIS

    @pyqtSlot()
    def save(self):
        try:
            self.tileWH = int(self.tileWHEdit.text())
        except:
            return QtWidgets.QMessageBox.about(self, 'Error','Size can only be a number')
        if self.listFiles.count() == 0:
            QtWidgets.QMessageBox.about(self, 'Error','You didn\'t picked a folder or that folder doesn\'t have any valid image format')
        else:
            self.selecfile = self.directory + '/' + self.listFiles.currentItem().text()
        if self.nameEdit.text() == "":
            QtWidgets.QMessageBox.about(self, 'Error','You didn\'t wrote a name to your file!')
        else:
            if self.listWidget.currentItem().text() == "TAR TileMap":
                if int(self.tileWHEdit.text()) > 100:
                    question = QtWidgets.QMessageBox.question(self,'Alert','Your tiles have more than 100x100 pixels. Continue?')
                    if question == QtWidgets.QMessageBox.Yes:
                        self.TARTilemap(self.selecfile)
                else:
                    self.TARTilemap(self.selecfile)

    def cancel(self):
        self.close()
    
    def refresh(self):
        self.tileWHEdit.setText(str(self.horizontalSlider.value()))
    
    def pickfolder(self):
        self.directory = QtWidgets.QFileDialog(self).getExistingDirectory()
        if self.directory != "":
            self.refreshdir()
