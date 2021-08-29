from PyQt5.QtCore import QObject, pyqtSignal


class StartClientWorker(QObject):
    progress = pyqtSignal(str)
    app = None
    cmd = ""

    def __init__(self, app, cmd=""):
        super().__init__()
        self.app = app
        self.cmd = cmd

    def run(self):
        self.app.startClient(self.progress, self.cmd)
