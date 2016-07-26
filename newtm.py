from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class newtmWindow(QtWidgets.QDialog):
    def __init__(self):
        super(newtmWindow,self).__init__()
        uic.loadUi('UI/newtm.ui', self)
        self.tileWHEdit.setText(str(self.horizontalSlider.value()))
        self.saveBox.accepted.connect(self.save)
        self.saveBox.rejected.connect(self.cancel)
        self.horizontalSlider.valueChanged.connect(self.refresh)
    
    @pyqtSlot()
    def save(self):
        try:
            self.tileWH = int(self.tileWHEdit.text())
        except:
            return QtWidgets.QMessageBox.about(self, 'Error','Size can only be a number')
        if self.nameEdit.text() == "":
            QtWidgets.QMessageBox.about(self, 'Error','You didn\'t wrote a name to your file!')
        else:
            pass

    def cancel(self):
        self.close()
    
    def refresh(self):
        self.tileWHEdit.setText(str(self.horizontalSlider.value()))
