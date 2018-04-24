#!/usr/bin/python3

import sys

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QListWidgetItem

GUI_FOLDER = '../res/ui/'

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(GUI_FOLDER + 'launchDialog.ui', self)
        # Disable unusued buttons
        self.opnProjBtn.setDisabled(True)
        self.convProjBtn.setDisabled(True)
        self.convTmBtn.setDisabled(True)
        self.settBtn.setDisabled(True)
        # Proper text on buttons
        self.newProjBtn.setText("New Project")
        self.opnProjBtn.setText("Open Project")
        self.convProjBtn.setText("Convert Project")
        self.newTmBtn.setText("New Tilemap")
        self.convTmBtn.setText("Convert Tilemap")
        self.settBtn.setText("Settings")
        # Proper text on the label
        self.formatsListLabel.setText("Available formats")
        # Map formats for the list
        self.availableFormats = [
            {
                "name": "Mapuche v1",
                "text": "A simple map format.\n Too limited for professional use."
            }
            ]
        for format in self.availableFormats:
            item = QListWidgetItem(format["name"])
            self.formatsListWidget.addItem(item)
        self.formatsListWidget.item(0).setSelected(True)
        # Show the description for the selected format
        self.updateDescription()
        # Signals
        self.formatsListWidget.itemSelectionChanged.connect(self.updateDescription)

    @pyqtSlot()
    def updateDescription(self):
        formName = self.formatsListWidget.selectedItems()[0].text()
        for i in self.availableFormats:
            if i["name"] == formName:
                text = i["text"]
                break
        self.formatInfoLabel.setText(text)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
