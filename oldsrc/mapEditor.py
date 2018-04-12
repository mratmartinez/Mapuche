import os
import sys
import struct
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
        # This should take the brush as the default 
        self.brushRadio.setChecked(True)
        # I will instance this here because I fucked up
        self.triggerEditorInstance = triggerEditorWindow()
        # A Tool Button for loading tilemaps and stuff
        self.toolButton.setPopupMode(2)
        # Since I don't know how to load this stuff properly, I'll improvise.
        menu = QMenu()
        actions = ['Load Tilemap', 'Load map', 'Triggers', 'Save Map',
                  'Load Old Map']
        for i in actions:
            menu.addAction(i)
        del(actions)
        menuActions = menu.actions()
        self.loadTmAction = menuActions[0]
        self.loadMapAction = menuActions[1]
        self.triggersAction = menuActions[2]
        self.saveMap = menuActions[3]
        self.pickOldMapAction = menuActions[4]
        self.toolButton.setMenu(menu)
        self.toolButton.setArrowType(Qt.DownArrow)
        self.tileMapFlag = False
        self.mapFileFlag = False
        # Signals
        self.loadTmAction.triggered.connect(self.pickTilemap)
        self.loadMapAction.triggered.connect(self.pickMap)
        self.triggersAction.triggered.connect(self.triggerEditor)
        self.saveMap.triggered.connect(self.saveMapFile)
        self.pickOldMapAction.triggered.connect(self.pickOldMap)
        self.mapFileViewer.itemSelectionChanged.connect(self.paint)

    def closeEvent(self, event):
        # We need to delete the temporary folder after we close the window.
        # Remember that when we delete the folder we also delete the saved map
        # because I was too lazy to add a Save To dialog. Also, it was
        # pointless since I was going to delete it with the project manager.
        for i in os.listdir(self.tmp_dir):
            os.remove(os.path.join(self.tmp_dir, i))
        os.removedirs(self.tmp_dir)
        event.accept()

    def untar(self, mapfile):
        # Obviously, it creates a temporary folder and load the tilemap there.
        tmp_dir = tempfile.mkdtemp()
        tar = tarfile.open(mapfile)
        tar.extractall(tmp_dir)
        self.loadTilemap(tmp_dir)

    def loadTilemap(self, tmp_dir):
        # For some reason, I didn't defined tmp_dir in the whole instance.
        self.tmp_dir = tmp_dir
        # We need to take the metadata of the file to know what kind of map we
        # are going to load.
        config = configparser.ConfigParser()
        config.read(os.path.join(self.tmp_dir, 'metafile.ini'))
        columns = int(config['META']['COLUMNS'])
        rows = int(config['META']['ROWS'])
        self.blankTile = config['META']['BLANKTILE']
        self.tileSize = int(config['META']['TILESIZE'])
        self.columnLabel.setText('Columns: ' + str(columns))
        self.rowLabel.setText('Rows: ' + str(rows))
        # Well, this is adapting both viewers for the tiles size and giving the
        # tilemap viewer the proper number of columns and rows.
        self.tileMapViewer.setIconSize(QSize(self.tileSize, self.tileSize))
        self.mapFileViewer.setIconSize(QSize(self.tileSize, self.tileSize))
        self.tileMapViewer.setColumnCount(columns)
        self.tileMapViewer.setRowCount(rows)
        for column in range(0, columns):
            self.tileMapViewer.setColumnWidth(column, self.tileSize)
            for row in range (0, rows):
                self.tileMapViewer.setRowHeight(row, self.tileSize)
                # Turned out this will work without the '.png'
                filename = str(column) + '-' + str(row) + '.png'
                filedir = os.path.join(self.tmp_dir, filename)
                icon = QIcon(filedir)
                item = QTableWidgetItem(icon, None)
                self.tileMapViewer.setItem(row, column, item)
        # This flag is to avoid errors with people trying to load the map
        # without loading the tilemap first
        self.tileMapFlag = True
        selected = self.blankTile.split('-')
        self.tileMapViewer.setCurrentCell(int(selected[1]), int(selected[0]))

    @pyqtSlot()
    def pickTilemap(self):
        # FUCK ALL THIS FILTERS SYSTEM. FUCK YOU, Qt!
        filters = 'TAR (*.tar);;TAR + GZip (*.tar.gz);;\
                 TAR + BZip2 (*.tar.bz2);; TAR + LZMA (*.tar.xz)'
        mapfile = QFileDialog().getOpenFileName(filter = filters)
        if mapfile != '':
            self.untar(mapfile[0])

    def setBrush(self):
        # This is useless atm.
        self.tileMapViewer.setSelectionMode(1)

    def paint(self):
        # This will paint the map tile. But take in count that this uses an
        # unproper (or at least proper but not unique) signal that won't paint
        # the last selected tile.
        itemRow = self.tileMapViewer.currentRow()
        itemColumn = self.tileMapViewer.currentColumn()
        filename = str(itemColumn) + '-' + str(itemRow)
        filedir = os.path.join(self.tmp_dir, filename)
        icon = QIcon(filedir)
        item = QTableWidgetItem(icon, None)
        row = self.mapFileViewer.currentRow()
        column = self.mapFileViewer.currentColumn()
        self.mapFileViewer.setItem(row, column, item)
        self.currentMap[column][row] = filename

    def triggerEditor(self):
        self.triggerEditorInstance.show()

    def pickMap(self):
        # Did I said that the filters system is a FUCKING SHIT!?
        # Why? Really shitty syntax! And also the documentations doesn't help
        # making it easier.
        filters = 'Mapuche v1 unwritten (*.mu1);;\
                    Mapuche v1 (*.mv1)'
        # Here we load a *.mu1 file, which would be the "Project Meta" in the
        # next version. That's the reason we have to load this one first,
        # without the TRIGGERS section.
        # Also, this just fills the whole map with the blank tile.
        mapfile = QFileDialog().getOpenFileName(filter = filters)
        if (mapfile[0] != '') & self.tileMapFlag:
            config = configparser.ConfigParser()
            config.read(os.path.join(self.tmp_dir, mapfile[0]))
            self.mapSize = int(config['META']['SIZE'])
            self.layers = int(config['META']['LAYERS'])
            self.mapFileViewer.setColumnCount(self.mapSize)
            self.mapFileViewer.setRowCount(self.mapSize)
            self.currentMap = list()
            for c in range(0, self.mapSize):
                self.currentMap.append(list())
                self.mapFileViewer.setColumnWidth(c, self.tileSize)
                for r in range(0, self.mapSize):
                    self.currentMap[c].append(self.blankTile)
                    self.mapFileViewer.setRowHeight(r, self.tileSize)
                    filename = self.blankTile # + '.png'
                    filedir = os.path.join(self.tmp_dir, filename)
                    icon = QIcon(filedir)
                    item = QTableWidgetItem(icon, None)
                    self.mapFileViewer.setItem(r, c, item)
            self.mapFileFlag = True
            self.mapFile = mapfile[0]

    def pickOldMap(self):
        # This would be the definitive way to load maps. In this case we load
        # the *.mv1 files.
        filters = 'Mapuche v1 unwritten (*.mu1);;\
                    Mapuche v1 (*.mv1)'
        mapfile = QFileDialog().getOpenFileName(filter = filters)
        if (mapfile[0] != '') & self.tileMapFlag:
            config = configparser.ConfigParser()
            # On a Python interpreter, we wouldn't need to catch the exception.
            # The error is not a bad thing, because it's the config parser
            # catching all that binary stuff that can't read and freaking out
            # because of that.
            # As I said, on a terminal, it works fine. But, on the project, it
            # crashes. So we need to tell ConfigParser that it shouldn't be a
            # pussy.
            try:
                config.read(os.path.join(self.tmp_dir, mapfile[0]),
                            'unicode_escape')
            except configparser.ParsingError:
                    pass # Come on, ConfigParser, don't be a pussy!
            self.mapSize = int(config['META']['SIZE'])
            self.layers = int(config['META']['LAYERS'])
            triggerQ = int(config['TRIGGERS']['QUANTITY'])
            # Forgot to do this, but with the Global and Local Triggers system,
            # I would have to write it again anyway.
            # TODO Load triggers
            self.mapFileViewer.setColumnCount(self.mapSize)
            self.mapFileViewer.setRowCount(self.mapSize)
            self.currentMap = list()
            with open(mapfile[0], 'rb') as loadedMap:
                # The 8 is the minimum number of lines with metadata. I will
                # have to add a line for the tilemap when I create the Project
                # Manager.
                for i in range(0, 8 + triggerQ):
                    # I don't know if there is a better way to do this, reading
                    # the lines with this is so fucking uncool.
                    loadedMap.readline()
                for c in range(0, self.mapSize):
                    self.currentMap.append(list())
                    self.mapFileViewer.setColumnWidth(c, self.tileSize)
                    for r in range(0, self.mapSize):
                        col, row = struct.unpack('BB',
                                                 loadedMap.read1(2))
                        tile = str(row) + '-' + str(col)
                        self.currentMap[c].append(tile)
                        self.mapFileViewer.setRowHeight(r, self.tileSize)
                        # At this point, after seeing another part where I
                        # forgot the '.png' thing, I realized that it worked
                        # without it. Magic.
                        filename = tile # + '.png'
                        filedir = os.path.join(self.tmp_dir, filename)
                        icon = QIcon(filedir)
                        item = QTableWidgetItem(icon, None)
                        self.mapFileViewer.setItem(r, c, item)
            # I don't remember the reason of this flag. Looks good.
            self.mapFileFlag = True
            self.mapFile = mapfile[0]

    def saveMapFile(self):
        # Now I remember
        if not self.mapFileFlag:
            return
        rows = self.triggerEditorInstance.triggerTableWidget.rowCount()
        # I don't care if you want to create more maps. 'map.mv1' is all you
        # need. Before it's deleted with the rest of the folder.
        filename = 'map.mv1'
        directory = self.tmp_dir
        filedir = os.path.join(directory, filename)
        # It's a good thing that I made this triggers dictionary. Because I
        # didn't used it in the end.
        triggerDict = dict()
        for i in range(0, rows):
            it = self.triggerEditorInstance.triggerTableWidget.item(0,i)
            triggerDict.update({i: str(it.text())})
        with open(self.mapFile, 'r') as formatFile:
            METADATA = formatFile.read() + '\n'
        METADATA = METADATA + (
            "[TRIGGERS]\n"
            "QUANTITY = {0}\n"
        ).format(len(triggerDict))
        for i in triggerDict:
            METADATA = METADATA + (
                "EVENT" + str(i) + " = " + triggerDict[i] + "\n"
            )
        # Without this, ConfigParser will take the binary part too
        METADATA += "[END]\n\n"
        with open(filedir, 'w') as tmpMap:
            tmpMap.write(METADATA)
        with open(filedir, 'ab') as tmpMap:
            for c in range(0, self.mapSize):
                for r in range(0, self.mapSize):
                    row, col = self.currentMap[c][r].split('-')
                    # Yeah, I could have written this in just one line, but I
                    # like it more this way.
                    bcol = struct.pack('B', int(col))
                    brow = struct.pack('B', int(row))
                    tmpMap.write(bcol)
                    tmpMap.write(brow)

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
        self.buttonBox.accepted.connect(self.saveProgress)

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

    def saveProgress(self):
        self.hide()

class addTriggerWindow(QDialog):
    def __init__(self):
        # We need this to load the GUI
        super(addTriggerWindow, self).__init__()
        uic.loadUi(os.path.join(GUI_FOLDER, 'addTrigger.ui'), self)
