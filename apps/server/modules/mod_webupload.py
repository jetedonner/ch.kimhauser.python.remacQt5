import requests
from apps.server.modules.libs.mod_interface import mod_interface


class mod_webupload(mod_interface):

    cmd_short = "wu"
    cmd_long = "webupload"
    cmd_desc = "Web Upload module"

    def setup_mod(self):
        print(f'Module Setup (mod_webupload) called successfully!')

    def run_mod(self, cmd="", param=""):
        # url = 'https://www.facebook.com/favicon.ico'
        # saveAsFilePath = './tmp/facebook.ico'
        # args = param.split(' ')
        #
        # if len(args) >= 2:
        #     url = args[0]
        #     saveAsFilePath = args[1]
        #
        # r = requests.get(url, allow_redirects=True)
        # open(saveAsFilePath, 'wb').write(r.content)dd

        url = 'http://www.kimhauser.ch/uploadz/uploadz.php'
        filename = "./tmp/index.html"
        with open(filename, 'rb') as f:
            r = requests.post(url, files={'filename':('index.html', f)})
            rx = r

        return f'Webload module uploaded url: {url} to: {filename}!'

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Web Upload' module uploads a file from the\n"
                                     "servers filesystem to a url in the web with POST.\n"
                                     ""),
            'cmd': f'{self.getCmdVariants4Help()} <filename_to_upload> <upload_url>',
            'ext': self.pritify4log(
                    '<filename_to_upload> specifies the filename to upload.\n'
                    '<upload_url> is the target url where to POST the file to.\n')
        }
        return help_txt
