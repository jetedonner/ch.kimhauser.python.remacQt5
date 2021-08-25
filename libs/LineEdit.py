from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt


class LineEdit(QLineEdit):
    upPressed = pyqtSignal()
    downPressed = pyqtSignal()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Up:
            self.upPressed.emit()
        elif event.key() == Qt.Key_Down:
            self.downPressed.emit()
