from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_chrome_login(mod_client_interface):

    cmd_short = "cl"
    cmd_long = "chromelogin"
    cmd_desc = "Chrome login client module"

    def setup_mod(self):
        print(f'Module Setup (mod_client_chrome_login) called successfully!')

    def run_mod(self, message):
        return f"Client mod_client_chrome_login module answered: \n{super(mod_client_chrome_login, self).run_mod(message)}"
