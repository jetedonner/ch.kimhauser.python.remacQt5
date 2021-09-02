from apps.server.modules.libs.mod_interface import mod_interface


class mod_help(mod_interface):
    def setup_mod(self):
        print(f'Module Setup (mod_help) called successfully!')

    def run_mod(self, cmd=""):
        print(f'Help Module')
        return f'Help module called!'

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Help' module returns a string with the\n"
                                     "help information about the reMac-App. You will\n"
                                     "find the available commands and functions."),
            'cmd': 'hp',
            'ext': 'This command has no arguments'
        }
        return help_txt
