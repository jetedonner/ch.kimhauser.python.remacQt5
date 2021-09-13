from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_args(mod_client_interface):

    cmd_short = "ar"
    cmd_long = "args"
    cmd_desc = "Args client module"

    def setup_mod(self):
        print(f'Module Setup (mod_client_args) called successfully!')

    def run_mod(self, message):
        return f"Client args module answered:\n{super(mod_client_args, self).run_mod(message)}"
