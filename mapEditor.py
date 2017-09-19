import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import (QDialog, QMessageBox, 
                            QFileDialog, QMenu, QAction)

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
        self.loadTmAction.triggered.connect(self.loadTilemap)

    def loadTilemap(self):
        print("Working")
