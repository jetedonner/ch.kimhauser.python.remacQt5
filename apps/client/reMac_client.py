import socket
import selectors
import traceback
import base64

from apps.client.libs.reMac_libclient import reMac_libclient

conHost = "192.168.0.49"
# conHost = "127.0.0.1"
conPort = "6890"

sel = selectors.DefaultSelector()


class reMac_client:

    my_client_lib = None
    prg = None
    DEFAULT_ACTION = "mh"

    def __init__(self):
        self.setup_client()

    def setup_client(self):
        print(f'Client setup successfully!')

    def getModule4Cmd(self, cmd):
        for md in reMac_libclient.reMacModules:
            if md.cmd_short.startswith(cmd) or md.cmd_long.startswith(cmd):
                return md
        return None

    def create_request(self, action, value):
        mod = self.getModule4Cmd(action)
        if mod is not None:
            return dict(
                type="text/json",
                encoding="utf-8",
                content=dict(action=action, value=value),
            )
        elif action == "ul":
            filename = value.split("/")[-1]
            file_obj = open(value, 'rb')
            file_bytes = file_obj.read()
            file_64_encode = base64.encodebytes(file_bytes)
            file_obj.close()
            return dict(
                type="text/json",
                encoding="utf-8",
                content=dict(action=action, value=dict(filename=filename, data=file_64_encode.decode("utf-8"))),
            )
        elif action == "sh":
            self.prg.emit("$: ")
        else:
            return dict(
                type="binary/custom-client-binary-type",
                encoding="binary",
                content=bytes(action + ": " + value, encoding="utf-8"),
            )

    def start_connection(self, host, port, request):
        retVal = False
        addr = (host, port)
        print("reMac Client - Starting connection to:", addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.settimeout(5)  # 5 seconds
        try:
            sock.connect_ex(addr)
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
             # reMac_libclient(sel, sock, addr, request)
            message = reMac_libclient(sel, sock, addr, request, self.prg)
            self.my_client_lib = message
            sel.register(sock, events, data=message)
            retVal = True
        except socket.error as exc:
            print(f"Caught exception socket.error: {exc}")
        return retVal

    def send2_client(self, msg=DEFAULT_ACTION, valz="", myHost=conHost, myPort=conPort):
        self.start_client(myHost, myPort, msg, valz)

    def start_client(self, myHost=conHost, myPort=conPort, prg=None, msg=DEFAULT_ACTION, valz=""):
        self.prg = prg
        try:
            host, port = myHost, int(myPort)
            action, value = msg, valz
            if action == "":
                action = self.DEFAULT_ACTION
            args = action.split(" ", 1)
            if len(args) >= 2:
                value = args[1]
            request = self.create_request(args[0].lower(), value)
            connResult = self.start_connection(host, port, request)
            # prg.emit(f"Connection to reMac Server ({conHost}:{conPort}) successfully established!")
            try:
                while True:
                    events = sel.select(timeout=1)
                    for key, mask in events:
                        message = key.data
                        try:
                            message.process_events(mask)
                        except Exception:
                            print(
                                "main: error: exception for",
                                f"{message.addr}:\n{traceback.format_exc()}",
                            )
                            message.close()
                    # Check for a socket being monitored to continue.
                    if not sel.get_map():
                        break
            except KeyboardInterrupt:
                print("caught keyboard interrupt, exiting")
        except Exception:
            print(
                "ERROR: Connection to reMac Server: {conHost}:{conPort} failed!",
                f"\nException: {traceback.format_exc()}",
            )
            return False
