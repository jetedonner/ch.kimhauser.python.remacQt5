from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_clipboard(mod_client_interface):

    cmd_short = "cb"
    cmd_long = "clipboard"
    cmd_desc = "Clipboard client module"

    def setup_mod(self):
        print(f'Module Setup (mod_client_clipboard) called successfully!')

    def run_mod(self, message):
        return f"{super(mod_client_clipboard, self).run_mod(message)}"
