import os
import sys
import cv2
import hashlib
import tempfile

from PyQt5 import uic
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import (
            QListWidgetItem, QDialog, QFileDialog, QMessageBox)
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QSize

GUI_FOLDER = './UI/'
MIN_TILE_SIZE = 16
MAX_TILE_SIZE = 128
DEFAULT_TILE_SIZE = 32


# First, we'll define the properties
class TAR():
    def __init__(self):
        self._format = 'TAR'
        self._extension = '.tar'

    def show(self, resource, tileSize):
        return(TARWindow(resource, tileSize))

    @property
    def getformat(self):
        return(self._format)

    def getextenstion(self):
        return(self._extension)


class newTilemapWindow(QDialog):
    def __init__(self):
        # We need this to load the GUI
        super(newTilemapWindow, self).__init__()
        uic.loadUi(GUI_FOLDER + 'newTm.ui', self)
        # Defining labels
        self.formatLabel.setText('Format:')
        self.resourcesLabel.setText('Tiles Resources:')
        self.tileNameLabel.setText('Tilemap Name:')
        self.tileSizeSlider.setSliderPosition(DEFAULT_TILE_SIZE)
        self.updateSizeLabel()
        # And tileSizeSlider range should be the same than
        # the constants indicate.
        # Also, it should have a proper default position.
        self.tileSizeSlider.setMinimum(MIN_TILE_SIZE)
        self.tileSizeSlider.setMaximum(MAX_TILE_SIZE)
        # Accepted resource formats
        self.resourceSuffix = ('.png', '.bmp', '.jpg')
        # Now we should define the available formats
        self.formatList = {
                            'TAR Tilemap': 'TAR'
                            }
        # And add the formats into the widget
        for f in list(self.formatList):
            item = QListWidgetItem(f)
            self.formatListWidget.addItem(item)
            if f == list(self.formatList)[0]:
                self.formatListWidget.setCurrentItem(item)
        # Signals and slots
        self.chooseButton.clicked.connect(self.pickFolder)
        self.tileSizeSlider.valueChanged.connect(self.updateSizeLabel)
        self.saveBox.accepted.connect(self.saveTilemap)
        self.saveBox.rejected.connect(self.cancel)

    # This method load the items in the resourceListWidget.
    def refreshdir(self, d):
        files = os.listdir(d)
        for i in files:
            for j in self.resourceSuffix:
                if i.lower().endswith(j):
                    item = QListWidgetItem(i)
                    self.resourceListWidget.addItem(item)
            if i == files[0]:
                self.resourceListWidget.setCurrentItem(item)
        self.directory = d

    @pyqtSlot()
    def pickFolder(self):
        directory = QFileDialog().getExistingDirectory()
        if directory != '':
            return(self.refreshdir(directory))

    def updateSizeLabel(self):
        self.tileSizeLabel.setText('Tiles Size: '
                                # Under-indented on purpose
                                + str(self.tileSizeSlider.value()))

    def saveTilemap(self):
        if self.nameLineEdit.text() == '':
            QMessageBox.about(self, 'Error',
                        # Under-indented on purpose
                        "You didn't wrote a name to your tilemap!")
        elif not self.resourceListWidget.currentItem():
            QMessageBox.about(self, 'Error',
                    # Under-indented on purpose
                    "You didn't selected a resource for your tilemap!")
        else:
            d = self.formatListWidget.currentItem().text()
            method = getattr(sys.modules[__name__], self.formatList[d])
            selectedResource = (str(self.directory)
                        # Under-indented on purpose
                        + '/'
                        + self.resourceListWidget.currentItem().text())
            tileSize = self.tileSizeSlider.value()
            self.instance = method().show(selectedResource, tileSize)
            self.instance.show()

    def cancel(self):
        self.close()


class TARWindow(QDialog):
    def __init__(self, resource, size):
        # Load UI
        super(TARWindow, self).__init__()
        uic.loadUi(GUI_FOLDER + 'tarCreation.ui', self)
        self.resource = cv2.imread(resource)
        self.h, self.w = self.resource.shape[:2]
        self.tileSize = size
        # We'll need a temporal folder
        self.tmp_dir = tempfile.mkdtemp()
        # In order to get the tiles we'll define the size
        self.resourceView.setIconSize(QSize(size, size))
        # Defining labels
        self.comprLabel.setText('Compression:')
        self.getTiles(self.resource, self.h, self.w, self.tileSize)
        self.refreshdir()

    def getTiles(self, resource, h, w, tileSize):
        o = 0
        for i in range(0, h, tileSize):
            p = 0
            for j in range(0, w, tileSize):
                box = self.resource[i:i+tileSize, j:j+tileSize]
                nm = str(o) + '-' + str(p) + '.png'
                place = os.path.join(self.tmp_dir, nm)
                cv2.imwrite(place, box)
                p += 1
            o += 1

    def hashsum(self, path, hex=True, hash_type=hashlib.md5):
        hashinst = hash_type()
        blocksize = hashinst.block_size * 128
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(blocksize), b''):
                hashinst.update(chunk)
        return(hashinst.hexdigest() if hex else hashinst.digest())

    def removeRepeated(self):
        unique = []
        for filename in os.listdir(self.tmp_dir):
            fileplace = os.path.join(self.tmp_dir, filename)
            filehash = self.hashsum(fileplace)
            if filehash not in unique:
                unique.append(filehash)
            else:
                os.remove(fileplace)

    def refreshdir(self):
        self.removeRepeated()
        files = os.listdir(self.tmp_dir)
        files.sort()
        for filename in files:
            icon = QIcon(os.path.join(self.tmp_dir, filename))
            item = QListWidgetItem(icon, None)
            self.resourceView.addItem(item)
