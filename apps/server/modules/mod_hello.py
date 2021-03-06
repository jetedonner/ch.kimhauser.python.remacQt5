from datetime import datetime
from apps.server.modules.libs.mod_interface import mod_interface


class mod_hello(mod_interface):

    cmd_short = "hw"
    cmd_long = "helloworld"
    cmd_desc = "Hello World module"

    def setup_mod(self):
        print(f'Module Setup (mod_hello) called successfully!')

    def run_mod(self, cmd="", param=""):
        print(f'Hello Module')
        now = datetime.now()
        return f'HelloWorld module called @ {now.strftime("%m/%d/%Y, %H:%M:%S")}!'

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Hello World' module just returns a string from\n"
                                     "the server to the client and acts as test function\n"
                                     "call to check the connection."),
            'cmd': f'{self.getCmdVariants4Help()}',
            'ext': 'This command has no arguments'
        }
        return help_txt
