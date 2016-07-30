from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QSize
from PIL import Image
import os, tempfile

class TARWindow(QtWidgets.QDialog):
    def __init__(self, resource):
        super(TARWindow,self).__init__()
        uic.loadUi('UI/tartm.ui', self)
        self.tmp_dir = tempfile.mkdtemp()
        self.resource = Image.open(resource)
        self.h, self.w = self.resource.size
    
    def refreshdir(self):
        files = os.listdir(self.tmp_dir)
        files.sort()        
        for i in files:
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
        self.items = ["TAR TileMap PNG"]
        for i in self.items:
            self.listWidget.addItem(i)

    def refreshdir(self):
        files = os.listdir(self.directory)
        files.sort()
        for i in files:
            if (i.lower().endswith('.png') or i.lower().endswith('.bmp')):
                self.listFiles.addItem(i)

    def TARTilemap(self, resource):
        self.tarfile = TARWindow(resource)
        for i in range(0,self.tarfile.h,self.tileWH):
            for j in range(0,self.tarfile.w,self.tileWH):
                box = (j,i,j+self.tileWH,i+self.tileWH)
                try:
                    res = self.tarfile.resource.crop(box)
                    res.save(self.tarfile.tmp_dir + '/' + str(j) + str(i),"png")
                except:
                    pass
        self.tarfile.show()
        self.tarfile.resourceView.setIconSize(QSize(self.tileWH,self.tileWH))
        self.tarfile.refreshdir()

    @pyqtSlot()
    def save(self):
        try:
            self.tileWH = int(self.tileWHEdit.text())
        except:
            return QtWidgets.QMessageBox.about(self, 'Error','Size can only be a number')
        if self.listFiles.count() == 0:
            return QtWidgets.QMessageBox.about(self, 'Error','You didn\'t picked a folder or that folder doesn\'t have any valid image format')
        elif self.listFiles is None:
            return QtWidgets.QMessageBox.about(self, 'Error','You didn\'t picked a resource file!')
        elif self.nameEdit.text() == "":
            return QtWidgets.QMessageBox.about(self, 'Error','You didn\'t wrote a name to your file!')
        else:
            self.selecfile = self.directory + '/' + self.listFiles.currentItem().text()
            if self.listWidget.currentItem().text() == "TAR TileMap PNG":
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
