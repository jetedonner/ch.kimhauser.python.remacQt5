from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_module_help(mod_client_interface):
    def setup_mod(self):
        print(f'Module Setup (mod_client_module_help) called successfully!')

    def run_mod(self, message):
        return f"Server mod_client_module_help module answered: {super(mod_client_module_help, self).run_mod(message)}"
