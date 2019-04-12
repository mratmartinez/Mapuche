#!/usr/bin/python3

import os
import sys

import json
import logging

import cv2
import tarfile
import tempfile
from zipfile import ZipFile
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QRegExp, QSize
from PyQt5.QtGui import QRegExpValidator, QIcon
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QListWidgetItem, QButtonGroup,
    QFileDialog, QDialogButtonBox, QMessageBox, QTableWidgetItem

)

GUI_FOLDER = '../res/ui/'
SUPPORTED_FORMATS = ('.bmp', '.jpeg', '.jpg', '.jpe', '.png', '.tiff',
                     '.tif', '.jp2', '.pbm', '.pgm', '.ppm', '.sr', '.ras')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(GUI_FOLDER + 'launchDialog.ui', self)
        # Disable unusued buttons
        self.settBtn.setDisabled(True)
        # Proper text on buttons
        self.newProjBtn.setText("New Project")
        self.opnProjBtn.setText("Open Project")
        self.settBtn.setText("Settings")
        # Let's instance the newProjectDialog before it's too late
        self.newProjectInstance = newProjectDialog()
        # Signals
        self.newProjBtn.clicked.connect(self.createNewProject)
        self.opnProjBtn.clicked.connect(self.openProject)

    @pyqtSlot()
    def createNewProject(self):
        self.newProjectInstance.show()

    def openProject(self):
        directory = QFileDialog().getExistingDirectory()
        self.mapEditorInstance = MapEditor(directory)
        self.mapEditorInstance.show()


class newProjectDialog(QDialog):
    def __init__(self):
        super(newProjectDialog, self).__init__()
        uic.loadUi(GUI_FOLDER + 'newProject.ui', self)
        self.saveFolder = None
        self.selectedFlag = False
        # Text for the labels
        self.tileMapsQuantityLabel.setText("Tilemaps:")
        self.triggersQuantityLabel.setText("Triggers:")
        self.projectNameLabel.setText("Project Name:")
        self.mapQuantityLabel.setText("Maps:")
        self.mapDefSizeLabel.setText("Map Size:")
        self.triggersBtn.setText("Event Triggers:")
        self.destinationBtn.setText("Destination Folder")
        self.addTmBtn.setText("Add Tilemap")
        self.selectedTmsLabel.setText("Selected Tilemaps")
        self.remTmBtn.setText("Remove Tilemaps")
        self.updateTilemapsQuantity()
        self.updateButtonStatus()
        # Set defaults
        self.mapQuantityInput.setMinimum(1)
        self.mapQuantityInput.setMaximum(10000)
        self.mapDefSizeInput.setMinimum(5)
        self.mapDefSizeInput.setMaximum(10000)
        self.tileSizeInput.setValue(32)
        self.tileSizeInput.setMinimum(16)
        # Validator
        self.projectNameLineEdit.setMaxLength(16)
        self.nameValidator = QRegExpValidator(QRegExp("[\w\-. ]+$"),
                                              self.projectNameLineEdit)
        self.projectNameLineEdit.setValidator(self.nameValidator)
        # Signals
        self.projectNameLineEdit.textChanged.connect(self.updateButtonStatus)
        self.addTmBtn.clicked.connect(self.pickFile)
        self.remTmBtn.clicked.connect(self.delSelected)
        self.destinationBtn.clicked.connect(self.changeFolder)
        self.buttonBox.accepted.connect(self.saveFiles)

    @pyqtSlot()
    def updateTilemapsQuantity(self):
        tilemaps = self.tmsListWidget.count()
        logger.info(tilemaps)
        self.tmQuantLabel.setText(str(tilemaps))

    @pyqtSlot()
    def updateButtonStatus(self):
        if self.projectNameLineEdit.text() == str() or not self.saveFolder or self.tmsListWidget.count() == 0:
            self.buttonBox.buttons()[0].setDisabled(True)
        else:
            self.buttonBox.buttons()[0].setDisabled(False)

    @pyqtSlot()
    def changeFolder(self):
        directory = QFileDialog().getExistingDirectory()
        if directory != '':
            self.saveFolder = directory
        self.updateButtonStatus()

    @pyqtSlot()
    def pickFile(self):
        filelist = QFileDialog().getOpenFileNames()[0]
        tilelist = []
        for i in filelist:
            if i.lower().endswith(SUPPORTED_FORMATS) and self.itemcheck(i):
                tilelist.append(i)
        logger.info(tilelist)
        self.tmsListWidget.addItems(tilelist)
        self.updateButtonStatus() # Qt doesn't provide the kind of signal I need for this case.

    @pyqtSlot()
    def delSelected(self):
        item = self.tmsListWidget.currentRow()
        self.deleteItem(item)

    def deleteItem(self, item):
        deleted = self.tmsListWidget.takeItem(self.tmsListWidget.currentRow())
        # We need to manually delete this object from memory
        del deleted

    # Qt should provide a method for doing this efficiently automatically
    def itemcheck(self, item):
        for i in range(0, self.tmsListWidget.count()):
            if self.tmsListWidget.item(i).text() == item:
                return False
        return True

    @pyqtSlot()
    def saveFiles(self):
        # Metadata
        filecount = self.tmsListWidget.count()
        name = self.projectNameLineEdit.text()
        folder = os.path.join(self.saveFolder, name)
        tilesize = self.tileSizeInput.value()
        mapquantity = self.mapQuantityInput.value()
        mapsize = self.mapDefSizeInput.value()
        logger.info((filecount, name, folder, tilesize, mapquantity, mapsize))
        # Preparations
        resfolder = os.path.join(folder, "res")
        mapsfolder = os.path.join(folder, "maps")
        outfolder = os.path.join(folder, "out")
        os.mkdir(folder)
        os.mkdir(resfolder)
        os.mkdir(mapsfolder)
        os.mkdir(outfolder)
        for i in range(0, filecount):
            inbreedfolder = os.path.join(resfolder, str(i))
            os.mkdir(inbreedfolder)
            c, r = self.cropImage(self.tmsListWidget.item(i), tilesize, inbreedfolder)
            data = {"columns": c, "rows": r, "size": tilesize}
            with open(os.path.join(inbreedfolder, "data.json"), "w") as file:
                json.dump(data, file)
        maplayer = [[[0, 0, 0] for j in range(0, mapsize)] for k in range(0, mapsize)]
        emptylayer = [[[] for j in range(0, mapsize)] for k in range(0, mapsize)]
        mapdata = {"layer0": maplayer,
                "layer1": emptylayer,
                "layer2": emptylayer,
                "layer3": emptylayer,
                "triggers": emptylayer}
        for i in range(0, mapquantity):
            with open(os.path.join(mapsfolder, str(i) + ".json"), "w") as file:
                json.dump(mapdata, file)

    def cropImage(self, file, size, folder):
        image = cv2.imread(file.text())
        h, w = image.shape[:2]
        r = 0 # rows
        for i in range(0, h, size):
            c = 0 # columns
            for j in range(0, w, size):
                box = image[i:i+size, j:j+size]
                nm = str(c) + '-' + str(r) + '.png'
                place = os.path.join(folder, nm)
                cv2.imwrite(place, box)
                c += 1
            r += 1
        return(c,r)


class MapEditor(QMainWindow):
    def __init__(self, project=None):
        super(MapEditor, self).__init__()
        uic.loadUi(GUI_FOLDER + 'mapEditor.ui', self)
        buttonGroup = QButtonGroup()
        buttonGroup.addButton(self.layer0Btn)
        buttonGroup.addButton(self.layer1Btn)
        buttonGroup.addButton(self.layer2Btn)
        buttonGroup.addButton(self.layer3Btn)
        buttonGroup.addButton(self.trigBtn)
        self.layer0Btn.setText("Layer 0")
        self.layer1Btn.setText("Layer 1")
        self.layer2Btn.setText("Layer 2")
        self.layer3Btn.setText("Layer 3")
        self.trigBtn.setText("Triggers")
        self.mapListLabel.setText("Maps")
        self.tilemapListLabel.setText("Tilemaps")
        self.tileMapWidget.setSortingEnabled(False)
        if project:
            self.loadProject(project)

    def loadProject(self, folder):
        self.loadTilemaps(os.path.join(folder, "res"))
        # self.loadMaps()

    def loadTilemapData(self, folder):
        tilemaps = list()
        for i in os.listdir(folder):
            with open(os.path.join(os.path.join(folder, i), "data.json"), "r") as metadata:
                data = json.load(metadata)
            self.tileMapWidget.setRowCount(data["rows"])
            self.tileMapWidget.setColumnCount(data["columns"])
            self.tileMapWidget.setIconSize(QSize(data["size"], data["size"]))
            tilemaps.append(data)
        return tilemaps

    def createIcon(self, file):
        icon = QIcon(file)
        item = QTableWidgetItem(icon, None)
        return item

    def loadTilemaps(self, folder):
        tilemaps = self.loadTilemapData(folder)
        for i in range(0, len(tilemaps)):
            data = tilemaps[i]
            c = data["columns"]
            r = data["rows"]
            size = data["size"]
            for column in range(c):
                self.tileMapWidget.setColumnWidth(column, size)
                for row in range(r):
                    self.tileMapWidget.setRowHeight(row, size)
                    setfolder = os.path.join(folder, str(i))
                    filename = str(column) + '-' + str(row)
                    filepath = os.path.join(setfolder, filename + ".png")
                    logger.debug(filepath)
                    item = self.createIcon(filepath)
                    self.tileMapWidget.setItem(row, column, item)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
