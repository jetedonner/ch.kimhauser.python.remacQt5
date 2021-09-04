from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_shellcmd(mod_client_interface):

    cmd_short = "sh"
    cmd_long = "shellcmd"
    cmd_desc = "Shell command client module"

    def setup_mod(self):
        print(f'Module Setup (mod_client_shellcmd) called successfully!')
