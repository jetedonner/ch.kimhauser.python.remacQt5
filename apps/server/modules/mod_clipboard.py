import clipboard
from apps.server.modules.libs.mod_interface import mod_interface


class mod_clipboard(mod_interface):
    def setup_mod(self):
        print(f'Module Setup (mod_clipboard) called successfully!')

    def run_mod(self, cmd = ""):
        clipboard_content = clipboard.paste()
        print(f'Clipboard content: {clipboard_content}')
        return clipboard_content
