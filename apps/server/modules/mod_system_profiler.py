import platform
import os
import socket
import fcntl
import struct

from apps.server.modules.libs.mod_interfaceRunCmd import mod_interfaceRunCmd


class mod_system_profiler(mod_interfaceRunCmd):

    cmd_short = "sp"
    cmd_long = "sysprofiler"
    cmd_desc = "System profiler module"

    cmd_sys_prof = "system_profiler | more"
    # cmd_uname_long = "uname -a"

    def setup_mod(self):
        print(f'Module Setup (mod_system_profiler) called successfully!')

    def run_mod(self, cmd="", param=""):
        sRet = f'#========================================================================#\n'
        sRet += f' System profiler for server - IP: {self.get_hostIP()}\n'
        sRet += self.get_sys_prof()
        # if param == "" or param == "-m" or param == "-a":
        #     sRet += f"| Host: " + socket.gethostname() + "\n"
        # if param == "" or param == "-m" or param == "-a":
        #     sRet += f"| System: " + self.get_model()
        # if param == "" or param == "-p" or param == "-a":
        #     sRet += f"| Platform: " + self.get_platform() + "\n"
        # if param == "" or param == "-v" or param == "-a":
        #     sRet += f"| macOS version: " + self.get_macVer() + "\n"
        # if param == "" or param == "-vv" or param == "-a":
        #     arrVers = self.get_vers()
        #     strVers = arrVers.replace("\n", "\n| ")
        #     sRet += f"| macOS v. ext.: \n| " + strVers + "\n"
        # if param == "" or param == "-u" or param == "-a":
        #     sRet += f"| Current user: {self.get_user()}\n"
        # if param == "" or param == "-s" or param == "-a":
        #     sRet += f"| {self.get_sip()}"
        #     if param == "-s":
        #         sRet += "\n"
        # if param == "" or param == "-w" or param == "-wl" or param == "-a":
        #     sRet += f"| WiFi: \n" + self.get_wifi(True)
        # if param == "-ws":
        #     sRet += f"| WiFi: \n" + self.get_wifi(False)
        # if param == "" or param == "-b" or param == "-a":
        #     sRet += ("|" if param == "-b" else  "") + f" Battery: " + self.get_battery()
        # if param != "-v" and param != "-m" and param != "-p" and param != "-u":
        #     sRet = sRet[:-1]
        sRet += f'#========================================================================#\n'
        return sRet

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'System profiler' module returns extended\n"
                                     "information about the server system."),
            'cmd': f'{self.getCmdVariants4Help()}',
            'ext': self.pritify4log(
                   'This module has no params')
        }
        return help_txt

    def get_hostIP(self):
        myIP = "127.0.0.1"
        addrInfo = socket.getaddrinfo(socket.gethostname(), None, family=socket.AF_INET, proto=socket.IPPROTO_TCP)
        addrInfoNG = addrInfo

        for hn in addrInfo:
            if hn[4][0] != myIP:
                myIP = hn[4][0]
                break

        return myIP

    def get_sys_prof(self):
        return self.run_command(self.cmd_sys_prof)
