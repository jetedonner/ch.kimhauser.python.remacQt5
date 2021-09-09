from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QTextBrowser, QPushButton, QCheckBox, QApplication
from ui.libs.LineEdit import LineEdit
from PyQt5.QtCore import QSettings


class pref_dialog(QDialog):

    app = QApplication([])

    txtTimeout = LineEdit()
    chkKeepAlive = QCheckBox("Keep connection alive")
    chkAddTimestamp = QCheckBox("Add timestamp to result")
    chkOpenImagePreview = QCheckBox("Open images preview")

    settings = QSettings("kimhauser.ch", "reMacQt5")

    def __init__(self):
        super().__init__()

    def initUI(self, settings):
        self.settings = settings
        # lblHelpTitle = QLabel("Help")
        layoutMain = QVBoxLayout()

        layoutMain.addWidget(self.chkKeepAlive)
        self.chkKeepAlive.setChecked(bool(self.settings.value("keepalive", False, bool)))

        layoutMain.addWidget(self.chkAddTimestamp)
        self.chkAddTimestamp.setChecked(bool(self.settings.value("addTimestamp", True, bool)))

        layoutMain.addWidget(QLabel("Timeout:"))
        self.txtTimeout.setPlaceholderText("Timeout (sec)")
        layoutMain.addWidget(self.txtTimeout)
        self.txtTimeout.setText(str(self.settings.value("timeout", 120, int)))

        layoutMain.addWidget(self.chkOpenImagePreview)
        self.chkOpenImagePreview.setChecked(bool(self.settings.value("openimagepreview", True, bool)))
        # layoutMain.addWidget(lblHelpTitle)
        # txtHelpContent = QTextBrowser()
        # txtHelpContent.setOpenExternalLinks(True)
        # txtHelpContent.setFixedHeight(500)
        # txtHelpContent.setFixedWidth(600)
        # # txtHelpContent.setFontFamily("Courier")
        # # txtHelpContent.setFontPointSize(14)
        # # txtHelpContent.setFontWeight(25)  # QtGui.QFont.Normal)
        # txtHelpContent.setReadOnly(True)
        #
        # help_file = open(f'help.html', 'rb')
        # help_txt = help_file.read()
        #
        # txtHelpContent.setHtml(help_txt.decode("utf-8"))
        # layoutMain.addWidget(txtHelpContent)
        cmdClose = QPushButton("Close")
        cmdClose.clicked.connect(self.closeDialog)
        layoutMain.addWidget(cmdClose)
        self.setWindowTitle("reMac v0.0.1 - Preferences")
        self.setFixedWidth(300)
        self.setLayout(layoutMain)
        self.setModal(True)
        # self.focusWidget()

    def showDialog(self):
        self.show()
        self.exec_()

    def closeDialog(self):
        self.settings.setValue("timeout", self.txtTimeout.text())
        self.settings.setValue("keepalive", bool(self.chkKeepAlive.isChecked()))
        self.settings.setValue("addTimestamp", bool(self.chkAddTimestamp.isChecked()))
        self.settings.setValue("openimagepreview", bool(self.chkOpenImagePreview.isChecked()))
        self.close()
