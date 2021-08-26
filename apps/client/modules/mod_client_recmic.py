import os
import base64
import time
from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_recmic(mod_client_interface):
    def setup_mod(self):
        print(f'Module Setup (mod_client_recmic) called successfully!')

    def get_datetime_str(self):
        return time.strftime("%Y%m%d-%H%M%S")

    def run_mod(self, message):
        result = super(mod_client_recmic, self).run_mod(message)
        print(result)
        cur_dir = os.path.abspath("./tmp")
        base64ToolContent = result
        base64ToolContent = base64ToolContent.encode()
        audio_out = f"{cur_dir}/recmic-{self.get_datetime_str()}.mp3"
        with open(audio_out, "wb") as output_file:
            output_file.write(base64.b64decode(base64ToolContent))
        return f"Recorded mic audio saved to: {audio_out}"
