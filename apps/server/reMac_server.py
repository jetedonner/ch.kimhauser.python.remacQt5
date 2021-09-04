import socket
import selectors
import traceback
import sys
import threading
# import keyboard
from pynput import keyboard
# import queue
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from apps.server.libs import reMac_libserver

conHost = "192.168.0.49"
# conHost = "127.0.0.1"
conPort = "6890"

sel = selectors.DefaultSelector()


class reMac_server():
    global lsock
    lsock = None
    prgng = None

    # conHost = "127.0.0.1"
    # conPort = "6890"

    def __init__(self):
        self.setup_server()

    # somewhere accessible to both:
    # callback_queue = queue.Queue()

    # def from_dummy_thread(self, func_to_call_from_main_thread):
    #     reMac_server.callback_queue.put(func_to_call_from_main_thread)

    def setup_server(self):
        print(f'Server setup successfully!')

    def accept_connection(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        print("accepted connection from", addr)
        if self.prgng is not None:
            self.prgng.emit(f"accepted connection from: {addr}")

        conn.setblocking(False)
        message = reMac_libserver.reMac_libserver(sel, conn, addr)
        sel.register(conn, selectors.EVENT_READ, data=message)

    def on_press(self, key):
        if key.char == None:
            return
        if key == keyboard.Key.esc or key.char == 'q':
            # Stop listener
            self.doExit = True
            # message.close()
            # sel.close()
            sys.exit(1)
            # return False
        # else:
        #     _start()

    def start_server(self, myHost=conHost, myPort=conPort, prg=None, prgng=None):
        self.prgng = prgng
        conHost, conPort = myHost, int(myPort)
        self.start_server_thread(conHost, conPort, prg)

    def stop_server(self):
        if lsock is not None:
            lsock.close()

    def start_server_thread(self, conHost, conPort, prg = None):
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        lsock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        lsock.bind((conHost, conPort))
        lsock.listen()
        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ, data=None)
        prg.emit(2)
        # with keyboard.Listener(on_press=self.on_press) as listener:
        #     listener.join()

        try:
            while True:
                # if self.doExit:
                #     break
                events = sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_connection(key.fileobj)
                    else:
                        message = key.data
                        try:
                            sret = message.process_events(mask)
                            if sret is not None and sret != "":
                                self.prgng.emit(sret)
                        except Exception:
                            print(
                                "main: error: exception for",
                                f"{message.addr}:\n{traceback.format_exc()}",
                            )
                            message.close()
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            sel.close()
