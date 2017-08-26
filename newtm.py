from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import QListWidgetItem
import os, tempfile, hashlib, cv2

class TARWindow(QtWidgets.QDialog):
    def __init__(self, resource):
        super(TARWindow,self).__init__()
        uic.loadUi('UI/tartm.ui', self)
        self.tmp_dir = tempfile.mkdtemp()
        self.resource = cv2.imread(resource)
        self.h, self.w, self.channels = self.resource.shape
        del(self.channels)
    
    def refreshdir(self):
        self.remove_blanks()
        files = os.listdir(self.tmp_dir)
        files.sort()        
        for filename in files:
            icon = QIcon(os.path.join(self.tmp_dir, filename))
            item = QListWidgetItem(icon, None)
            self.resourceView.addItem(item)

    def hashsum(self, path, hex=True, hash_type=hashlib.md5):
        hashinst = hash_type()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(hashinst.block_size * 128), b''):
                hashinst.update(chunk)
        return hashinst.hexdigest() if hex else hashinst.digest()

    def remove_blanks(self):
        unique = []
        for filename in os.listdir(self.tmp_dir):
            fileplace = os.path.join(self.tmp_dir, filename)
            filehash = self.hashsum(fileplace)
            if filehash not in unique: 
                unique.append(filehash)
            else:
                os.remove(fileplace)

class newtmWindow(QtWidgets.QDialog):
    def __init__(self):
        super(newtmWindow,self).__init__()
        uic.loadUi('UI/newtm.ui', self)
        self.tileWHEdit.setValidator(QIntValidator(10,100))
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
            if (i.lower().endswith('.png') or i.lower().endswith('.bmp') or i.lower().endswith('.jpg')):
                self.listFiles.addItem(i)

    def TARTilemap(self, resource):
        self.tarfile = TARWindow(resource)
        a = 0
        for i in range(0,self.tarfile.h,self.tileWH):
            b = 0
            for j in range(0,self.tarfile.w,self.tileWH):
                box = self.tarfile.resource[i:i+self.tileWH,j:j+self.tileWH]
                try:
                    name = str(a) + '-' + str(b) + '.png'
                    place = os.path.join(self.tarfile.tmp_dir, name)
                    cv2.imwrite(place, box)
                except:
                    print("Nismanea3")
                b += 1
            a += 1
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
