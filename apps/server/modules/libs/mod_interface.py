class mod_interface:
    def __init__(self):
        self.setup_mod()

    def setup_mod(self):
        pass

    def run_mod(self, cmd = ""):
        pass

    def mod_helptxt(self):
        help_txt = {
            'desc': 'dummy module help text',
            'cmd': '<dummy cmd>',
            'ext': '<dummy ext>'
        }
        return help_txt

    def pritify4log(self, text):
        return text.replace("\n", "\n| ")
