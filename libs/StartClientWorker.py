from PyQt5.QtCore import QObject, pyqtSignal


class StartClientWorker(QObject):
    progress = pyqtSignal(str)
    app = None

    def __init__(self, app):
        super().__init__()
        self.app = app

    def run(self):
        self.app.startClient(self.progress)
