import platform
import socket
from apps.server.modules.libs.mod_interfaceRunCmd import mod_interfaceRunCmd


class mod_info(mod_interfaceRunCmd):
    def setup_mod(self):
        print(f'Module Setup (mod_info) called successfully!')

    def run_mod(self, cmd = ""):
        print(f'Info Module')
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        sRet = f'#========================================================================#\n'
        sRet += f'| Info for server - IP: {local_ip}\n'
        sRet += f"| System: " + self.get_model()
        sRet += f"| macOS version: " + self.get_macVer() + "\n"
        sRet += f"| WiFi: \n" + self.get_wifi()
        sRet += f" Battery: " + self.get_battery()
        sRet += f'#========================================================================#\n'
        return sRet

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