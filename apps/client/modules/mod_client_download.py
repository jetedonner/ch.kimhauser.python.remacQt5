import os
import base64
import time
from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_download(mod_client_interface):
    def setup_mod(self):
        print(f'Module Setup (mod_client_download) called successfully!')

    def get_datetime_str(self):
        return time.strftime("%Y%m%d-%H%M%S")

    def run_mod(self, message):
        sresult = super(mod_client_download, self).run_mod(message)
        # return sresult
        # print(content.get("result"))
        cur_dir = os.path.abspath("./tmp")
        base64ToolContent = sresult#content.get("result")
        base64ToolContent = base64ToolContent.encode()
        sc_out = f"{cur_dir}/{message['filename']}"
        with open(sc_out, "wb") as output_file:
            output_file.write(base64.b64decode(base64ToolContent))
        return f"Downloaded file saved to: {sc_out}"
        # return f"Server mod_client_screenshot module answered: {s}"
