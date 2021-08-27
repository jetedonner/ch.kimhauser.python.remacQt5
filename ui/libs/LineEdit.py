from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt


class LineEdit(QLineEdit):
    upPressed = pyqtSignal()
    downPressed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.mimeData()
            # print(event.mimeData().text())
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            # links = []
            for url in event.mimeData().urls():
                # https://doc.qt.io/qt-5/qurl.html
                if url.isLocalFile():
                    self.setText("ul " + str(url.toLocalFile()))
                    break
                    # links.append(str(url.toLocalFile()))
                # else:
                #     links.append(str(url.toString()))
            # self.addItems(links)
        else:
            event.ignore()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Up:
            self.upPressed.emit()
        elif event.key() == Qt.Key_Down:
            self.downPressed.emit()
