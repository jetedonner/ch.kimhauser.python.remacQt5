from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_upload(mod_client_interface):

    cmd_short = "ul"
    cmd_long = "upload"
    cmd_desc = "Upload client module"

    def setup_mod(self):
        print(f'Module Setup (mod_client_upload) called successfully!')

    def run_mod(self, message):
        result = super(mod_client_upload, self).run_mod(message)
        return f"Upload returns: {result}"

