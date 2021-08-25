from apps.server.modules.libs.mod_interface import mod_interface


class mod_hello(mod_interface):
    def setup_mod(self):
        print(f'Module Setup (mod_hello) called successfully!')

    def run_mod(self, cmd = ""):
        print(f'Hello Module')
        return f'HelloWorld module called!'
