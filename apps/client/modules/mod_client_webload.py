from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_webload(mod_client_interface):

    cmd_short = "wl"
    cmd_long = "webload"
    cmd_desc = "Web Download client module"

    def setup_mod(self):
        print(f'Module Setup (mod_client_webload) called successfully!')

    def run_mod(self, message):
        return f"Client web download module answered: {super(mod_client_webload, self).run_mod(message)}"
