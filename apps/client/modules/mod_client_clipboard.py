from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_clipboard(mod_client_interface):
    def setup_mod(self):
        print(f'Module Setup (mod_client_clipboard) called successfully!')

    def run_mod(self, message):
        return f"{super(mod_client_clipboard, self).run_mod(message)}"
