import base64
import os
from apps.server.modules.libs.mod_interfaceRunCmd import mod_interfaceRunCmd


class mod_upload(mod_interfaceRunCmd):

    def setup_mod(self):
        print(f'Module Setup (mod_upload) called successfully!')

    def run_mod(self, cmd="", param=""):
        filename = param["filename"]
        data = param["data"]
        try:
            cur_dir = os.path.abspath("./tmp")
            base64ToolContent = data
            base64ToolContent = base64ToolContent.encode()
            sc_out = f"{cur_dir}/{filename}"
            with open(sc_out, "wb") as output_file:
                output_file.write(base64.b64decode(base64ToolContent))
                output_file.close()
            return f"Successfully uploaded file to {sc_out}"
        except OSError:
            return f"Error uploading file {filename}"
        return ""
