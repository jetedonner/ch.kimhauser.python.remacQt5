import platform
import socket
from apps.server.modules.libs.mod_interfaceRunCmd import mod_interfaceRunCmd


class mod_info(mod_interfaceRunCmd):
    def setup_mod(self):
        print(f'Module Setup (mod_info) called successfully!')

    def run_mod(self, cmd="", param=""):
        # print(f'Info Module')
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        sRet = f'#========================================================================#\n'
        sRet += f'| Info for server - IP: {local_ip}\n'
        if param == "" or param == "-m" or param == "-a":
            sRet += f"| System: " + self.get_model()
        if param == "" or param == "-v" or param == "-a":
            sRet += f"| macOS version: " + self.get_macVer() + "\n"
        if param == "" or param == "-w" or param == "-wl" or param == "-a":
            sRet += f"| WiFi: \n" + self.get_wifi(True)
        if param == "-ws":
            sRet += f"| WiFi: \n" + self.get_wifi(False)
        if param == "" or param == "-b" or param == "-a":
            sRet += ("|" if param == "-b" else  "") + f" Battery: " + self.get_battery()
        sRet = sRet[:-1]
        sRet += f'#========================================================================#\n'
        return sRet

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Info' module returns information about\n"
                                     "the server system like macOS version, pc model,\n"
                                     "wifi info or the battery condition."),
            'cmd': 'in [-a | -v | -m | -w | -wl | -ws | -b]',
            'ext': self.pritify4log(
                   '-a\tAll available information - the default (like no param)\n'
                   '-v\tOnly macOS version\n'
                   '-m\tSystem model <sysctl -n hw.model>\n'
                   '-w|-wl\tAll Wifi-Info\n'
                   '-ws\tBasic Wifi-Info only\n'
                   '-b\tInformation about the battery')
        }
        return help_txt

    def get_macVer(self):
        return str(platform.mac_ver()[0])

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