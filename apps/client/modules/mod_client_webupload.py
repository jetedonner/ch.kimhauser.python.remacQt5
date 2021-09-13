from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_webupload(mod_client_interface):

    cmd_short = "wu"
    cmd_long = "webupload"
    cmd_desc = "Web Upload client module"

    def setup_mod(self):
        print(f'Module Setup (mod_client_webupload) called successfully!')

    def run_mod(self, message):
        return f"Client web upload module answered: {super(mod_client_webupload, self).run_mod(message)}"
