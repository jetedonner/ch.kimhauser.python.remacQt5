from PyQt5.QtCore import QObject, pyqtSignal


class StartServerWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    progressng = pyqtSignal(str)

    app = None

    def __init__(self, app):
        super().__init__()
        self.app = app

    def run(self):
        self.app.startServer(self.progress, self.progressng)
        self.finished.emit()
