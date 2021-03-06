import socket
from apps.server.modules.libs.mod_interface import mod_interface


class mod_modHelp(mod_interface):

    cmd_short = "mh"
    cmd_long = "modhelp"
    cmd_desc = "Module help module"

    def setup_mod(self):
        print(f'Module Setup (mod_modHelp) called successfully!')

    def run_mod(self, cmd="", param=""):
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
            'cmd': f'{self.getCmdVariants4Help()} [<module_name> [-c]]',
            'ext': self.pritify4log(
                '-c\tOnly the command calling information and details for <module_name>'
            )
        }
        return help_txt

    def print_client_help(self, appName, reMacModules, module=None):
        args = module.split()
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        sRet = f'#========================================================================#\n'
        # sRet += f'| {appName} Server - IP: {local_ip}\n'
        sRet += f'| \n'
        if len(args) == 0:
            sRet += f'| Modules and command help (all active modules):\n'
            sRet += f'| \n'
            for mod in reMacModules:
                altCmd = mod.cmd_long
                cmdStr = f'{mod.cmd_short} / {mod.cmd_long}:'
                if len(cmdStr) > 16:
                    tabs = f'\t'
                else:
                    tabs = f'\t\t'
                sRet += f'| {cmdStr}{tabs}{mod.cmd_desc}\n'
            sRet += f'| \n'
            sRet += f'| Print help for specific module: mh <module>\n'
        elif len(args) >= 1:
            moduleFound = False
            for mod in reMacModules:
                if mod.cmd_short == args[0] or mod.cmd_long == args[0]:
                    sRet += f'| Help for module "{mod.cmd_short}" / "{mod.cmd_long}":\n'
                    sRet += f'| \n'
                    altCmd = mod.cmd_long
                    # sRet += f'| -{keyTmp} / {altCmd[1]}: {altCmd[2]}\n'
                    help_dict = mod.mod_helptxt()
                    if len(args) == 1 or (len(args) == 2 and args[1] != "-c"):
                        sRet += f'| Description:\n| {help_dict["desc"]}\n|\n'
                    sRet += f'| Usage: {help_dict["cmd"]}\n|\n'
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

