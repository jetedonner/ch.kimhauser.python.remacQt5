from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_info(mod_client_interface):

    cmd_short = "in"
    cmd_long = "info"
    cmd_desc = "Info client module"

    def setup_mod(self):
        print(f'Module Setup (mod_client_info) called successfully!')

