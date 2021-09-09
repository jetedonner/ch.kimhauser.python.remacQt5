import os
import base64
# from PIL import Image
from apps.server.modules.libs.mod_interfaceRunCmd import mod_interfaceRunCmd

OUTPUT_PATH = "/tmp"
OUTPUT_FILE = f"{OUTPUT_PATH}/sc_tmp.png"
TOOL_CMD = "screencapture -x"


class mod_screenshot(mod_interfaceRunCmd):

    cmd_short = "sc"
    cmd_long = "screenshot"
    cmd_desc = "Screenshot module"

    def setup_mod(self):
        print(f'Module Setup (mod_screenshot) called successfully!')

    def run_mod(self, cmd="", param=""):
        filename_path = ""
        if param != "":
            args = param.split(" ")
            if len(args) >= 2:
                if args[0] == "-f":
                    filename_path = args[1]

        return self.take_screenshot(filename_path)

    def take_screenshot(self, filepath=""):
        self.run_command(TOOL_CMD + " " + OUTPUT_FILE)
        image = open(OUTPUT_FILE, 'rb')
        image_read = image.read()
        image_64_encode = base64.encodebytes(image_read)
        print(f'Screenshot taken successfully!')
        os.remove(OUTPUT_FILE)
        return {'img': image_64_encode.decode("utf-8"), 'filename_path': filepath}

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Screenshot' module takes a screenshot of the current\n"
                                     "view from the server. The client retrieves the image and\n"
                                     "saves it in the '/tmp' folder as well as opens it in the default\n"
                                     "image preview app on the client. You can also specify a filename with\n"
                                     "the '-f <filename>' param to override the default save location."),
            'cmd': f'{self.getCmdVariants4Help()} [-f <local filename / -path>]',
            'ext': self.pritify4log(
                   '-f\tSpecify file-path / -name for saving the retrieved image.\n\n'
                   f'Default save location is {OUTPUT_PATH} (app-dir) and the image filename\n'
                   f'will be padded with a timestamp. You will get the filename / path \n'
                   f'displayed when the module returns.')
        }
        return help_txt
