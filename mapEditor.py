import os
import sys
import tarfile
import tempfile
import configparser

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt, QSize
from PyQt5.QtWidgets import (QDialog, QMessageBox, 
                            QFileDialog, QMenu, QAction,
                            QTableWidgetItem, QPushButton)

GUI_FOLDER = './UI/'

class mapEditorWindow(QDialog):
    def __init__(self):
        # We need this to load the GUI
        super(mapEditorWindow, self).__init__()
        uic.loadUi(os.path.join(GUI_FOLDER, 'mapEditor.ui'), self)
        # Defining radio buttons
        self.brushRadio.setText('Brush')
        self.rectangleRadio.setText('Rectangle')
        # A button for filling the whole map with a tile
        self.fillButton.setText('Fill Map')
        # Let's also define labels
        self.columnLabel.setText('Columns: -')
        self.rowLabel.setText('Rows: -')
        # A Tool Button for loading tilemaps and stuff
        self.toolButton.setPopupMode(2)
        menu = QMenu()
        actions = ['Load Tilemap', 'Triggers']
        for i in actions:
            menu.addAction(i)
        del(actions)
        menuActions = menu.actions()
        self.loadTmAction = menuActions[0]
        self.triggersAction = menuActions[1]
        self.toolButton.setMenu(menu)
        self.toolButton.setArrowType(Qt.DownArrow)
        # Signals
        self.loadTmAction.triggered.connect(self.pickTilemap)
        self.triggersAction.triggered.connect(self.triggerEditor)


    def untar(self, mapfile):
        tmp_dir = tempfile.mkdtemp()
        tar = tarfile.open(mapfile)
        tar.extractall(tmp_dir)
        self.loadTilemap(tmp_dir)

    def loadTilemap(self, tmp_dir):
        self.tmp_dir = tmp_dir
        config = configparser.ConfigParser()
        config.read(os.path.join(self.tmp_dir, 'metafile.ini'))
        columns = int(config['META']['COLUMNS'])
        rows = int(config['META']['ROWS'])
        self.blankTile = config['META']['BLANKTILE']
        self.tileSize = int(config['META']['TILESIZE'])
        self.columnLabel.setText('Columns: ' + str(columns))
        self.rowLabel.setText('Rows: ' + str(rows))
        self.tileMapViewer.setIconSize(QSize(self.tileSize, self.tileSize))
        self.tileMapViewer.setColumnCount(columns)
        self.tileMapViewer.setRowCount(rows)
        for column in range(0, columns):
            self.tileMapViewer.setColumnWidth(column, self.tileSize)
            for row in range (0, rows):
                self.tileMapViewer.setRowHeight(row, self.tileSize)
                filename = str(column) + '-' + str(row) + '.png'
                filedir = os.path.join(self.tmp_dir, filename)
                icon = QIcon(filedir)
                item = QTableWidgetItem(icon, None)


    @pyqtSlot()
    def pickTilemap(self):
        filters = 'TAR (*.tar);;TAR + GZip (*.tar.gz);;\
                 TAR + BZip2 (*.tar.bz2);; TAR + LZMA (*.tar.xz)'
        mapfile = QFileDialog().getOpenFileName(filter = filters)
        if mapfile != '':
            self.untar(mapfile[0])
            self.tileMapViewer.setItem(row, column, item)

    def triggerEditor(self):
        self.triggerEditorInstance = triggerEditorWindow()
        self.triggerEditorInstance.show()


class triggerEditorWindow(QDialog):
    def __init__(self):
        # We need this to load the GUI
        super(triggerEditorWindow, self).__init__()
        uic.loadUi(os.path.join(GUI_FOLDER, 'triggerEditor.ui'), self)
        # We need to define this because it won't work if we do it later
        self.addTriggerInstance = addTriggerWindow()
        # We should define the table properly
        self.triggerTableWidget.setColumnCount(1)
        # Default Trigger
        defTrig = QTableWidgetItem('blocked')
        self.saveTrigger(defTrig)
        # It shouldn't work without an item selected
        self.delTriggerButton.setDisabled(True)
        # This should work somehow
        self.newTriggerButton.clicked.connect(self.addTrigger)
        self.delTriggerButton.clicked.connect(self.delTrigger)
        self.triggerTableWidget.itemSelectionChanged.connect(
                                                self.activateDeletion)
        self.addTriggerInstance.buttonBox.clicked.connect(
                                                self.saveTrigger)

    @pyqtSlot()
    def activateDeletion(self):
        self.delTriggerButton.setEnabled(True)

    def addTrigger(self):
        self.addTriggerInstance.show()

    def delTrigger(self):
        current = self.triggerTableWidget.currentRow()
        self.triggerTableWidget.removeRow(current)
        if(self.triggerTableWidget.rowCount()) == 0:
            self.delTriggerButton.setDisabled(True)

    def saveTrigger(self, argItem):
        count = self.triggerTableWidget.rowCount()
        self.triggerTableWidget.setRowCount(count + 1)
        if type(argItem) != QPushButton:
            item = argItem
        else:
            trigger = self.addTriggerInstance.lineEdit.text()
            item = QTableWidgetItem(trigger)
            self.addTriggerInstance.close()
        self.triggerTableWidget.setItem(count, 0, item) 
        self.triggerTableWidget.resizeColumnsToContents()

class addTriggerWindow(QDialog):
    def __init__(self):
        # We need this to load the GUI
        super(addTriggerWindow, self).__init__()
        uic.loadUi(os.path.join(GUI_FOLDER, 'addTrigger.ui'), self)
