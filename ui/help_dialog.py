from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QTextBrowser, QPushButton

class help_dialog(QDialog):

    def __init__(self):
        super().__init__()

    def initUI(self):
        layoutMain = QVBoxLayout()
        txtHelpContent = QTextBrowser()
        txtHelpContent.setOpenExternalLinks(True)
        txtHelpContent.setFixedHeight(500)
        txtHelpContent.setFixedWidth(600)
        txtHelpContent.setReadOnly(True)

        help_file = open(f'help.html', 'rb')
        help_txt = help_file.read()

        txtHelpContent.setHtml(help_txt.decode("utf-8"))
        layoutMain.addWidget(txtHelpContent)
        cmdClose = QPushButton("Close")
        cmdClose.clicked.connect(self.closeDialog)
        layoutMain.addWidget(cmdClose)

        self.setWindowTitle("reMac v0.0.1 - Help")
        self.setLayout(layoutMain)
        self.setModal(True)
        self.focusWidget()
        self.show()

    def closeDialog(self):
        self.close()
