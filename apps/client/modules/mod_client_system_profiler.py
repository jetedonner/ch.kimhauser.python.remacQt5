from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_system_profiler(mod_client_interface):

    cmd_short = "sp"
    cmd_long = "systemprofiler"
    cmd_desc = "System profiler client module"

    def setup_mod(self):
        print(f'Module Setup (mod_client_system_profiler) called successfully!')

