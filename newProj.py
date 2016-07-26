from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class newProjWindow(QtWidgets.QDialog):
    def __init__(self):
        super(newProjWindow,self).__init__()
        uic.loadUi('UI/newProj.ui', self)
        #~ Designer doesn't have QFileDialog :C
        self.fileDialog = QtWidgets.QFileDialog(self)
        self.pushButton.clicked.connect(self.directory)
    
    @pyqtSlot()
    def directory(self):
        self.lineEdit.setText(self.fileDialog.getExistingDirectory())
