import platform
import os
import socket
import fcntl
import struct

from apps.server.modules.libs.mod_interfaceRunCmd import mod_interfaceRunCmd


class mod_info(mod_interfaceRunCmd):

    cmd_short = "in"
    cmd_long = "info"
    cmd_desc = "Info module"

    cmd_sw_vers = "sw_vers"
    cmd_uname_long = "uname -a"

    def setup_mod(self):
        print(f'Module Setup (mod_info) called successfully!')

    def run_mod(self, cmd="", param=""):
        # hostname = socket.gethostname()
        # local_ip = socket.gethostbyname(hostname)
        # self.get_hostName()
        sRet = f'#========================================================================#\n'
        sRet += f'| Info for server - IP: {self.get_hostIP()}\n'
        if param == "" or param == "-m" or param == "-a":
            sRet += f"| Host: " + socket.gethostname() + "\n"
        if param == "" or param == "-m" or param == "-a":
            sRet += f"| System: " + self.get_model()
        if param == "" or param == "-p" or param == "-a":
            sRet += f"| Platform: " + self.get_platform() + "\n"
        if param == "" or param == "-v" or param == "-a":
            sRet += f"| macOS version: " + self.get_macVer() + "\n"
        if param == "" or param == "-vv" or param == "-a":
            arrVers = self.get_vers()
            strVers = arrVers.replace("\n", "\n| ")
            sRet += f"| macOS v. ext.: \n| " + strVers + "\n"
        if param == "" or param == "-u" or param == "-a":
            sRet += f"| Current user: {self.get_user()}\n"
        if param == "" or param == "-s" or param == "-a":
            sRet += f"| {self.get_sip()}"
            if param == "-s":
                sRet += "\n"
        if param == "" or param == "-w" or param == "-wl" or param == "-a":
            sRet += f"| WiFi: \n" + self.get_wifi(True)
        if param == "-ws":
            sRet += f"| WiFi: \n" + self.get_wifi(False)
        if param == "" or param == "-b" or param == "-a":
            sRet += ("|" if param == "-b" else  "") + f" Battery: " + self.get_battery()
        if param != "-v" and param != "-m" and param != "-p" and param != "-u":
            sRet = sRet[:-1]
        sRet += f'#========================================================================#\n'
        return sRet

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Info' module returns information about\n"
                                     "the server system like macOS version, pc model,\n"
                                     "wifi info or the battery condition."),
            'cmd': f'{self.getCmdVariants4Help()} [-a|-m|-p|-v|-u|-s|-w|-wl|-ws|-b]',
            'ext': self.pritify4log(
                   '-a\tAll available information - the default (like no param)\n'
                   '-m\tSystem model <sysctl -n hw.model>\n'
                   '-p\tPlatform\n'
                   '-v\tOnly macOS version\n'
                   '-u\tOnly current username (and is root?)\n'
                   '-s\tIs SIP enabled\n'
                   '-w|-wl\tAll Wifi-Info\n'
                   '-ws\tBasic Wifi-Info only\n'
                   '-b\tInformation about the battery')
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

    def get_macVer(self):
        return str(platform.mac_ver()[0])

    def get_sip(self):
        return self.run_command("csrutil status")

    def get_vers(self):
        return self.run_command(self.cmd_sw_vers).strip()

    def get_platform(self):
        return self.run_command(self.cmd_uname_long).strip()

    def get_user(self):
        current_user = self.run_command("whoami").strip()
        isRoot = False
        if current_user == "root":
            isRoot = True
        return f'{current_user} (isRoot: {isRoot})'

    def get_model(self):
        return self.run_command("sysctl -n hw.model")#.decode('utf-8')

    def get_wifi(self, allinfo = True):
        if allinfo:
            command = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I" # | grep -w SSID"
        else:
            command = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | grep -w SSID"
        sRet = self.run_command(command).replace("\n", "\n|")
        return "| " + sRet.strip() #self.run_command(command)#.decode('utf-8')#.replace("SSID: ", "").strip()

    def get_battery(self):
        sRet = self.run_command("pmset -g batt").replace("\n", "\n| ").replace("\t", "\n| ")
        return sRet[:-1] #.decode("utf-8")# | egrep \"([0-9]+\\%).*\" -o | cut -f1 -d\';\'")