import base64
import os
from apps.server.modules.libs.mod_interfaceRunCmd import mod_interfaceRunCmd


class mod_upload(mod_interfaceRunCmd):

    cmd_short = "ul"
    cmd_long = "upload"
    cmd_desc = "Upload module"

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

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Upload' module uploads a file or folder from the\n"
                                     "client and save's it remotely on the server. You have to\n"
                                     "specify a local file/folder and can optionally specify a\n"
                                     "path / filename on the server's remote filesystem where to\n"
                                     "save the uploaded content with the '-f' param.\n"
                                     "IMPORTANT: You / the app will have write permission on this\n"
                                     "location to save the file remotely."),
            'cmd': 'ul <local filename/path> [-f <remote filename/path>]',
            'ext': self.pritify4log(
                   '-f\tSpecify file-path / -name for saving the uploaded file/folder.\n\n'
                   f'Default save location is /tmp (app-dir) and the uploaded content will\n'
                   f'have the same name as the original file/folder on the client.')
        }
        return help_txt