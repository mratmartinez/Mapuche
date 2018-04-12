import os
import sys

from PyQt5 import uic
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem

GUI_FOLDER = './UI/'
MAX_TILES = 950
MIN_TILES = 1


# First, we'll define the properties of our formats
class MA1():
    def __init__(self):
        self._format = 'MA1'

    @property
    def getformat(self):
        return(self._format)


class newMapWindow(QDialog):
    def __init__(self):
        # We need this to load the GUI
        super(newMapWindow, self).__init__()
        uic.loadUi(os.path.join(GUI_FOLDER, 'newMap.ui'), self)
        # Defining labels
        self.formatLabel.setText('Format:')
        self.layerLabel.setText('Layers: '
                                + str(self.layerSlider.value())
                                )
        self.geometryLabel.setText('Map Size (Max. '
                                    # Over-indented on purpose
                                    + str(MAX_TILES)
                                    + ' tiles)')
        self.projectNameLabel.setText('Project Name:')
        # sizeLineEdit should only accept integers
        self.sizeLineEdit.setValidator(QIntValidator(
                                        MIN_TILES,
                                        MAX_TILES))
        # Defining the available formats
        self.formatList = {
                        'Mapache v1': 'MA1'
                        }
        # Loading the defined formats in the list
        for f in list(self.formatList):
            item = QListWidgetItem(f)
            self.formatListWidget.addItem(item)
            if f == list(self.formatList)[0]:
                self.formatListWidget.setCurrentItem(item)
        # If we don't do this, there won't be a format selected
        # by default. And that would raise an error if the user
        # tried to save it without selecting one first

        # Connect signals with slots
        self.saveBox.accepted.connect(self.saveProject)
        self.layerSlider.valueChanged.connect(self.updateLabel)
        self.saveBox.rejected.connect(self.cancel)

    @pyqtSlot()
    def saveProject(self):
        # self.pickedFormat = self.formatsList[
        #                    self.formatsListWidget.currentItem().text()
        #                    ].getformat()
        mapSize = self.sizeLineEdit.text()
        layer = self.layerSlider.value()
        if self.nameLineEdit.text() == '':
            QMessageBox.about(self, 'Error',
                            # Under-indented on purpose
                            "You didn't wrote a name to your project!")
        else:
            filters = 'Mapuche v1 unwritten (*.mu1)'
            savefile = QFileDialog().getSaveFileName(filter = filters)
            METADATA = (
                        "[META]\n"
                        "SIZE = {0}\n"
                        "LAYERS = {1}\n"
                        ).format(mapSize, layer)
            with open(savefile[0] + '.mu1', 'w') as map:
                map.write(METADATA)
            self.close()

    def cancel(self):
        self.close()

    def updateLabel(self):
        self.layerLabel.setText('Layers: '
                                + str(self.layerSlider.value()))
