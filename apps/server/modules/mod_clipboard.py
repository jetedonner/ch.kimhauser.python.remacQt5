import clipboard
from apps.server.modules.libs.mod_interface import mod_interface


class mod_clipboard(mod_interface):

    cmd_short = "cb"
    cmd_long = "clipboard"
    cmd_desc = "Clipboard module"

    def setup_mod(self):
        print(f'Module Setup (mod_clipboard) called successfully!')

    def run_mod(self, cmd="", param=""):
        result = "Clipboard module: nothing done!"
        if param == "":
            clipboard_content = clipboard.paste()
            result = f'Clipboard content: {clipboard_content}'
            # print(result)
        else:
            args = param.split()
            if len(args) >= 1:
                if args[0] == "-i":
                    newval = ' '.join(args[1:]).replace("\"", "")
                    clipboard.copy(newval)
                    result = f'Clipboard replaced with: "{newval}"'
                    # print(result)
                elif args[0] == "-r":
                    clipboard_content = clipboard.paste()
                    result = f'Clipboard content: {clipboard_content}'
                    # print(result)
        return result

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Clipboard' module accesses the clipboard of the \n"
                                     "server and returns it's content. You can also inject\n"
                                     "a string into the servers clipboard with param '-i'"),
            'cmd': f'{self.getCmdVariants4Help()} [-r | -i "<string to inject>"]',
            'ext': self.pritify4log(
                   '-r\tRead the servers clipboard - the default (like no param)\n'
                   '-i\tInject a string into server clipboard (also empty string "")')
        }
        return help_txt