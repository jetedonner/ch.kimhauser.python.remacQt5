from PyQt5.QtWidgets import QDialog, QLabel, QGridLayout, QVBoxLayout, QTextBrowser, QWidget, QPushButton, \
    QCheckBox, QApplication, QTabWidget
from ui.libs.LineEdit import LineEdit
from PyQt5.QtCore import QSettings, Qt
from PyQt5 import QtGui


class pref_dialog(QDialog):

    listCmds = []
    listCheckBox = []

    app = QApplication([])

    cmdCheckAll = QPushButton("Check All")

    txtTimeout = LineEdit()
    chkKeepAlive = QCheckBox("Keep connection alive")
    chkAddTimestamp = QCheckBox("Add timestamp to result")
    chkOpenImagePreview = QCheckBox("Open images preview")

    settings = QSettings("kimhauser.ch", "reMacQt5")

    def __init__(self):
        super().__init__()

    def initUI(self, settings, modules):
        self.settings = settings

        layout = QVBoxLayout()
        wdgtGeneral = QWidget()
        wdgtModules = QWidget()
        tabWdgt = QTabWidget()
        tabWdgt.setFont(QtGui.QFont("Arial", 13))

        # lblHelpTitle = QLabel("Help")
        layoutMain = QVBoxLayout()
        layoutMain.setAlignment(Qt.AlignTop)
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
        cmdClose = QPushButton("Cancel")
        cmdClose.clicked.connect(self.closeDialog)
        cmdSave = QPushButton("Save")
        cmdSave.clicked.connect(self.saveDialog)
        # layoutMain.addWidget(cmdClose)
        self.setWindowTitle("reMac v0.0.1 - Preferences")
        # self.setFixedWidth(300)
        self.setMinimumWidth(300)
        # layoutServer.addWidget(txtOutputServer)
        wdgtGeneral.setLayout(layoutMain)
        tabWdgt.addTab(wdgtGeneral, QtGui.QIcon('res/images/homepage.png'), "General")

        self.listCmds = []
        self.listCheckBox = []
        self.listLabel = []
        for module in modules:
            self.listCmds.append(module.cmd_short)
            self.listCheckBox.append(module.cmd_long)
            self.listLabel.append(module.cmd_desc)
        grid = QGridLayout()

        for i, v in enumerate(self.listCheckBox):
            self.listCheckBox[i] = QCheckBox(v)
            self.listCheckBox[i].setChecked(bool(self.settings.value(f"activemodules/{self.listCmds[i]}", True, bool)))
            self.listLabel[i] = QLabel(self.listLabel[i])
            grid.addWidget(self.listCheckBox[i], i, 0)
            grid.addWidget(self.listLabel[i], i, 1)

        # self.button = QPushButton("Check CheckBox")
        # self.button.clicked.connect(self.checkboxChanged)
        # self.labelResult = QLabel()

        # grid.addWidget(self.button, 10, 0, 1, 2)
        # grid.addWidget(self.labelResult, 11, 0, 1, 2)
        wdgtModules.setLayout(grid)


        self.cmdCheckAll.clicked.connect(self.checkAll)
        grid.addWidget(self.cmdCheckAll)

        tabWdgt.addTab(wdgtModules, QtGui.QIcon('res/images/modules.png'), "Modules")

        layout.addWidget(tabWdgt)
        layout.addWidget(cmdClose)
        layout.addWidget(cmdSave)
        self.setLayout(layout)
        self.setModal(True)
        # self.focusWidget()

    def showDialog(self):
        self.show()
        self.exec_()

    def checkAll(self):
        setChecked = True
        if self.cmdCheckAll.text() == "Check All":
            self.cmdCheckAll.setText("Uncheck All")
        else:
            setChecked = False
            self.cmdCheckAll.setText("Check All")

        for i, v in enumerate(self.listCmds):
            self.listCheckBox[i].setChecked(setChecked)
        # self.settings.setValue("timeout", self.txtTimeout.text())
        # self.settings.setValue("keepalive", bool(self.chkKeepAlive.isChecked()))
        # self.settings.setValue("addTimestamp", bool(self.chkAddTimestamp.isChecked()))
        # self.settings.setValue("openimagepreview", bool(self.chkOpenImagePreview.isChecked()))
        # self.close()

    def closeDialog(self):
        # self.settings.setValue("timeout", self.txtTimeout.text())
        # self.settings.setValue("keepalive", bool(self.chkKeepAlive.isChecked()))
        # self.settings.setValue("addTimestamp", bool(self.chkAddTimestamp.isChecked()))
        # self.settings.setValue("openimagepreview", bool(self.chkOpenImagePreview.isChecked()))
        self.close()

    def saveDialog(self):
        self.settings.setValue("timeout", self.txtTimeout.text())
        self.settings.setValue("keepalive", bool(self.chkKeepAlive.isChecked()))
        self.settings.setValue("addTimestamp", bool(self.chkAddTimestamp.isChecked()))
        self.settings.setValue("openimagepreview", bool(self.chkOpenImagePreview.isChecked()))

        for i, v in enumerate(self.listCmds):
            print(f"{i}: {v} => {self.listCheckBox[i].isChecked()}")
            self.settings.setValue(f"activemodules/{v}", self.listCheckBox[i].isChecked())

        self.close()


