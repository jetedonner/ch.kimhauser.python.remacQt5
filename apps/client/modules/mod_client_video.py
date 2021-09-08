from apps.client.modules.libs.mod_client_interface import mod_client_interface


class mod_client_video(mod_client_interface):

    cmd_short = "vd"
    cmd_long = "video"
    cmd_desc = "Video client module"

    def setup_mod(self):
        print(f'Module Setup (mod_client_video) called successfully!')

    def run_mod(self, message):
        return f"Client video module answered: {super(mod_client_video, self).run_mod(message)}"
