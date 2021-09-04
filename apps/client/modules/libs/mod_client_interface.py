class mod_client_interface:

    cmd_short = "<cmd_short dummy>"
    cmd_long = "<cmd_long dummy>"
    cmd_desc = "<desc dummy>"

    def __init__(self):
        self.setup_mod()

    def setup_mod(self):
        pass

    def run_mod(self, message):
        return message["result"]
