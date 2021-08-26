from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_shellcmd(mod_client_interface):
    def setup_mod(self):
        print(f'Module Setup (mod_client_shellcmd) called successfully!')
