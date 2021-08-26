import socket
from apps.server.modules.libs.mod_interface import mod_interface


class mod_modHelp(mod_interface):
    def setup_mod(self):
        print(f'Module Setup (mod_modHelp) called successfully!')

    def run_mod(self, cmd = ""):
        print(f'Module Help')
        return f'mod_modHelp module called!'

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Module Help' module returns a list of al available\n"
                                     "modules (if you don't specify a <module_name>) or a\n"
                                     "detailed the help text for the specified <module_name>.\n"
                                     "This is a description, the calling convention as well as\n"
                                     "extra information if there is any. You can also only show\n"
                                     "the calling information with the '-c' argument"),
            'cmd': 'mh [<module_name> [-c]]',
            'ext': self.pritify4log(
                '-c\tOnly the calling information for <module_name>'
            )
        }
        return help_txt

    def print_client_help(self, appName, reMacModules, module = None):
        args = module.split()
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        sRet = f'#========================================================================#\n'
        # sRet += f'| {appName} Server - IP: {local_ip}\n'
        sRet += f'| \n'
        if len(args) == 0:
            sRet += f'| Modules and command help (all active modules):\n'
            for keyTmp in list(reMacModules):
                altCmd = reMacModules[keyTmp]
                sRet += f'| {keyTmp} / {altCmd[1]}:\t\t{altCmd[2]}\n'
            sRet += f'| \n'
            sRet += f'| Print help for specific module: mh <module>\n'
        elif len(args) >= 1:
            sRet += f'| Specific command help for module "{args[0]}":\n'
            sRet += f'| \n'
            moduleFound = False
            for keyTmp in list(reMacModules):
                if keyTmp == args[0]:
                    altCmd = reMacModules[keyTmp]
                    # sRet += f'| -{keyTmp} / {altCmd[1]}: {altCmd[2]}\n'
                    help_dict = altCmd[0].mod_helptxt()
                    sRet += f'| Description:\n| {help_dict["desc"]}\n|\n'
                    sRet += f'| Call: {help_dict["cmd"]}\n|\n'
                    sRet += f'| Details:\n| {help_dict["ext"]}\n'
                    # sRet += f'| \n'
                    # sRet += f'| Command: {altCmd[3]}\n'
                    moduleFound = True
                    break
            if not moduleFound:
                sRet += f'| Command / Module "{args[0]}" NOT FOUND!!!\n'
        sRet += f'| \n'
        sRet += f'#========================================================================#\n'
        return sRet

