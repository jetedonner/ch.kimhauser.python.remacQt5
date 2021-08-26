import os
import base64
import time
from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_screenshot(mod_client_interface):
    def setup_mod(self):
        print(f'Module Setup (mod_client_screenshot) called successfully!')

    def get_datetime_str(self):
        return time.strftime("%Y%m%d-%H%M%S")

    def run_mod(self, message):
        sresult = super(mod_client_screenshot, self).run_mod(message)
        # print(content.get("result"))
        cur_dir = os.path.abspath("./tmp")
        base64ToolContent = sresult#content.get("result")
        base64ToolContent = base64ToolContent.encode()
        sc_out = f"{cur_dir}/screenshot-{self.get_datetime_str()}.png"
        with open(sc_out, "wb") as output_file:
            output_file.write(base64.b64decode(base64ToolContent))
        return f"Screenshot saved to: {sc_out}"
        # return f"Server mod_client_screenshot module answered: {s}"