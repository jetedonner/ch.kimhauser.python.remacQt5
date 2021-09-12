import requests
from apps.server.modules.libs.mod_interface import mod_interface


class mod_webload(mod_interface):

    cmd_short = "wl"
    cmd_long = "webload"
    cmd_desc = "Web Download module"

    def setup_mod(self):
        print(f'Module Setup (mod_webload) called successfully!')

    def run_mod(self, cmd="", param=""):
        url = 'https://www.facebook.com/favicon.ico'
        saveAsFilePath = './tmp/facebook.ico'
        args = param.split(' ')

        if len(args) >= 2:
            url = args[0]
            saveAsFilePath = args[1]

        r = requests.get(url, allow_redirects=True)
        open(saveAsFilePath, 'wb').write(r.content)

        return f'Webload module downloaded url: {url} to: {saveAsFilePath}!'

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Web Download' module downloads a file from the\n"
                                     "web and saves it on the server with the given path- and\n"
                                     "filename."),
            'cmd': f'{self.getCmdVariants4Help()} <dl_url> <filename_to_save>',
            'ext': '<dl_url> is the weblink to download. <filename_to_save> is\n'
                   'the filename / -path to save the downloaded content to.'
        }
        return help_txt
