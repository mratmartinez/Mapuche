#!/usr/bin/python3

import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog

import newTm
import newMap
import mapEditor
from Pytes import pytes

GUI_FOLDER = './UI/'  # Where the .ui files are saved


class MainWindow(QDialog):
    def __init__(self):
        # We need this to load the GUI
        super(MainWindow, self).__init__()
        uic.loadUi(GUI_FOLDER + 'main.ui', self)
        # Disabled widgets
        self.mapPropBtn.setDisabled(True)
        self.layer4Radio.setDisabled(True)
        # Defining the other windows
        self.newMapInstance = newMap.newMapWindow()
        self.newTmInstance = newTm.newTilemapWindow()
        self.mapEditorInstance = mapEditor.mapEditorWindow()
        # Connect signals with slots
        self.openMapBtn.clicked.connect(self.openMap)
        self.newMapBtn.clicked.connect(self.newMapSpawn)
        self.newTmBtn.clicked.connect(self.newTmSpawn)
        self.loadTmBtn.clicked.connect(self.mapEditorSpawn)

    @pyqtSlot()
    def openMap(self):
        self.mapfile = QFileDialog(self).getOpenFileName(self,
                                            # Under-indented on purpose
                                            'Open File', '',
                                            'Mapache v1 Maps (*.ma1)')

    def newMapSpawn(self):
        self.newMapInstance.show()

    def newTmSpawn(self):
        self.newTmInstance.show()

    def mapEditorSpawn(self):
        self.mapEditorInstance.show()


# main function
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
