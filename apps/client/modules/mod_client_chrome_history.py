import json
from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_chrome_history(mod_client_interface):
    def setup_mod(self):
        print(f'Module Setup (mod_client_chrome_history) called successfully!')

    def run_mod(self, message):
        result = super(mod_client_chrome_history, self).run_mod(message)
        result = json.loads(result)
        result = json.dumps(result, indent=4, sort_keys=True)
        # result = json.dumps(result, indent=4, sort_keys=True)
        return f"Client mod_client_chrome_history module answered: \n{result}"
