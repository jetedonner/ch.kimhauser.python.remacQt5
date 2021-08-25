import socket
from apps.server.modules.libs.mod_interface import mod_interface


class mod_modHelp(mod_interface):
    def setup_mod(self):
        print(f'Module Setup (mod_modHelp) called successfully!')

    def run_mod(self, cmd = ""):
        print(f'Module Help')
        return f'mod_modHelp module called!'

    def print_client_help(self, appName, reMacModules, module = None):
        args = module.split()
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        sRet = f'#========================================================================#\n'
        sRet += f'| {appName} Server - IP: {local_ip}\n'
        sRet += f'| \n'
        if len(args) == 0:
            sRet += f'| Modules and command help (all active modules):\n'
            for keyTmp in list(reMacModules):
                altCmd = reMacModules[keyTmp]
                sRet += f'| -{keyTmp} / {altCmd[1]}:\t\t{altCmd[2]}\n'
            sRet += f'| \n'
            sRet += f'| Print help for specific module: mh <module>\n'
        elif len(args) >= 1:
            sRet += f'| Specific command help for module "{args[0]}":\n'
            sRet += f'| \n'
            moduleFound = False
            for keyTmp in list(reMacModules):
                if keyTmp == args[0]:
                    altCmd = reMacModules[keyTmp]
                    sRet += f'| -{keyTmp} / {altCmd[1]}: {altCmd[2]}\n'
                    sRet += f'| \n'
                    sRet += f'| Command: {altCmd[3]}\n'
                    moduleFound = True
                    break
            if not moduleFound:
                sRet += f'| Command / Module "{args[0]}" NOT FOUND!!!\n'
        # else:
        #     sRet += f'| Command / Module {args[1]} NOT FOUND\n'
        sRet += f'| \n'
        sRet += f'#========================================================================#\n'
        return sRet

