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
        if param == "" or param == "-w" or param == "-a":
            sRet += f"| WiFi: \n" + self.get_wifi()
        if param == "" or param == "-b" or param == "-a":
            sRet += f" Battery: " + self.get_battery()
        sRet += f'#========================================================================#\n'
        return sRet

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Info' module returns informations about\n"
                                     "the server system like macOS version, pc model,\n"
                                     "wifi info or the battery condition."),
            'cmd': 'in [-a | -v | -m | -w | -b]',
            'ext': self.pritify4log(
                   '-a\tAll available information - the default (like no param)\n'
                   '-v\tOnly macOS version\n'
                   '-m\tSystem model <sysctl -n hw.model>\n'
                   '-w\tAll Wifi-Infos\n'
                   '-b\tInformation about the battery')
        }
        return help_txt

    def get_macVer(self):
        return str(platform.mac_ver()[0])

    def get_model(self):
        return self.run_command("sysctl -n hw.model")#.decode('utf-8')

    def get_wifi(self):
        command = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I" # | grep -w SSID"
        sRet = self.run_command(command).replace("\n", "\n|")
        return "|" + sRet #self.run_command(command)#.decode('utf-8')#.replace("SSID: ", "").strip()

    def get_battery(self):
        sRet = self.run_command("pmset -g batt").replace("\n", "\n|")
        return sRet #.decode("utf-8")# | egrep \"([0-9]+\\%).*\" -o | cut -f1 -d\';\'")