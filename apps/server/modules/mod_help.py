import socket
from apps.server.modules.libs.mod_interface import mod_interface


class mod_help(mod_interface):

    cmd_short = "hp"
    cmd_long = "help"
    cmd_desc = "Help module"

    def setup_mod(self):
        print(f'Module Setup (mod_help) called successfully!')

    def run_mod(self, cmd="", param=""):
        print(f'Help Module')
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        sRet = f'\n\n#========================================================================#\n'
        sRet += f'| reMac Help module - IP: {local_ip}\n'
        sRet += f'| Created by Kim-David Hauser, (C.) 2021-09-02\n'
        sRet += f'| \n'
        sRet += f'| Description:\n'
        sRet += f'| The reMac suite is a remote access and administration tool for macOS.\n'
        sRet += f'| \n'
        sRet += f'| The suite consists of a server and a client part. You can use the\n'
        sRet += f'| scripts from within the terminal or start the GUI script and\n'
        sRet += f'| use the QT5 app to control server and client.\n'
        sRet += f'| \n'
        sRet += f'| This piece of software was built with the help of python and has a\n'
        sRet += f'| modular structure. This means that all the features you can use are\n'
        sRet += f'| embedded into their own and separate module. This setup not only makes\n'
        sRet += f'| it easier to get an overview of the functions and sources but also\n'
        sRet += f'| let''s you build and plugin new features easily by creating a new\n'
        sRet += f'| module by copying i.e. the hello world module and starting to add\n'
        sRet += f'| your own functionalities.\n'
        sRet += f'| \n'
        sRet += f'| Website:\n'
        sRet += f'| - https://github.com/jetedonner/ch.kimhauser.python.remacQt5\n'
        sRet += f'| - http://kimhauser.ch/index.php/projects/remac\n'
        sRet += f'| \n'
        sRet += f'| Credits:\n'
        sRet += f'| - ...\n'
        sRet += f'| - ...\n'
        sRet += f'| \n'
        sRet += f'#========================================================================#\n'
        return sRet

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Help' module returns a string with the\n"
                                     "help information about the reMac-App. You will\n"
                                     "find the available commands and functions."),
            'cmd': f'{self.getCmdVariants4Help()}',
            'ext': 'This command has no arguments'
        }
        return help_txt
