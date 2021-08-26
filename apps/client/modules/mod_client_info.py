from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_info(mod_client_interface):
    def setup_mod(self):
        print(f'Module Setup (mod_client_info) called successfully!')

