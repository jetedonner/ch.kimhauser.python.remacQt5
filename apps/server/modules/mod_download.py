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
