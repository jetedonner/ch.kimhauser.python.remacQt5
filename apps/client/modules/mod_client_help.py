from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_help(mod_client_interface):

    cmd_short = "hp"
    cmd_long = "help"
    cmd_desc = "Help client module"

    def setup_mod(self):
        print(f'Module Setup (mod_client_help) called successfully!')

    def run_mod(self, message):
        return f"Client help module answered: {super(mod_client_help, self).run_mod(message)}"
