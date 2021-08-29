import base64
from apps.server.modules.libs.mod_interfaceRunCmd import mod_interfaceRunCmd


class mod_download(mod_interfaceRunCmd):

    def setup_mod(self):
        print(f'Module Setup (mod_download) called successfully!')

    def run_mod(self, cmd="", param=""):
        try:
            file_to_download = open(param, 'rb')
            file_to_download_content = file_to_download.read()
            file_to_download.close()
            file_to_download_content_base64_encoded = base64.encodebytes(file_to_download_content)
            return file_to_download_content_base64_encoded.decode("utf-8")
        except OSError:
            pass
        return ""

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Download' module downloads a file or folder from the\n"
                                     "server and save's it locally on the client. You have to\n"
                                     "specify a remote file/folder and can optionally specify a\n"
                                     "path / filename on the client's local filesystem where to\n"
                                     "save the downloaded content with the '-f' param."),
            'cmd': 'dl <remote filename/path> [-f <local filename/path>]',
            'ext': self.pritify4log(
                   '-f\tSpecify file-path / -name for saving the retrieved file/folder.\n\n'
                   f'Default save location is /tmp (app-dir) and the downloaded content will\n'
                   f'have the same name as the original on the server.')
        }
        return help_txt