class mod_client_interface:
    def __init__(self):
        self.setup_mod()

    def setup_mod(self):
        pass

    def run_mod(self, message):
        return message["result"]
