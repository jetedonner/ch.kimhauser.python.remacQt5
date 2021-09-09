from apps.server.modules.libs.mod_interface import mod_interface
# from keylogger import Keylogger
# from keylogger import Keylogger

SEND_REPORT_EVERY = 60  # in seconds, 60 means 1 minute and so on
EMAIL_ADDRESS = "put_real_address_here@gmail.com"
EMAIL_PASSWORD = "put_real_pw"

class mod_keylogger(mod_interface):

    cmd_short = "kl"
    cmd_long = "keylogger"
    cmd_desc = "Keylogger module"

    def setup_mod(self):
        print(f'Module Setup (mod_keylogger) called successfully!')
        pass

    def run_mod(self, cmd="", param=""):
        print(f'mod_keylogger Module')
        # keyloggerVar = Keylogger(interval=60, report_method="file")
        # keyloggerVar.start()
        return f'mod_keylogger module called!'