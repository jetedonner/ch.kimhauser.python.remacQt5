from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_hello(mod_client_interface):
    def setup_mod(self):
        print(f'Module Setup (mod_client_hello) called successfully!')

    def run_mod(self, message):
        return f"Client hello module answered: {super(mod_client_hello, self).run_mod(message)}"
