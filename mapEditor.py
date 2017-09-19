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
                            QTableWidgetItem)

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
        actions = ['Load Tilemap']
        for i in actions:
            menu.addAction(i)
        del(actions)
        menuActions = menu.actions()
        self.loadTmAction = menuActions[0]
        self.toolButton.setMenu(menu)
        self.toolButton.setArrowType(Qt.DownArrow)
        # Signals
        self.loadTmAction.triggered.connect(self.pickTilemap)

    @pyqtSlot()
    def pickTilemap(self):
        filters = 'TAR (*.tar);;TAR + GZip (*.tar.gz);;\
                 TAR + BZip2 (*.tar.bz2);; TAR + LZMA (*.tar.xz)'
        mapfile = QFileDialog().getOpenFileName(filter = filters)
        if mapfile != '':
            self.untar(mapfile[0])

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
                self.tileMapViewer.setItem(row, column, item)
