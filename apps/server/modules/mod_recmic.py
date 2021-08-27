import pyaudio
import wave
import base64
import os

from apps.server.modules.libs.mod_interfaceRunCmd import mod_interfaceRunCmd

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output123.wav"


class mod_recmic(mod_interfaceRunCmd):
    def setup_mod(self):
        print(f'Module Setup (mod_recmic) called successfully!')

    def run_mod(self, cmd="", param=""):
        args = param.split(" ")
        if len(args) == 2:
            if args[0] == "-t":
                try:
                    RECORD_SECONDS = int(args[1])
                except Exception:
                    pass

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print(f"* recording ({RECORD_SECONDS} seconds)")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        myFrames = b''.join(frames)
        wf.writeframes(myFrames)
        wf.close()
        self.run_command("lame " + WAVE_OUTPUT_FILENAME + " " + WAVE_OUTPUT_FILENAME + ".mp3")

        base64ToolFile = open(WAVE_OUTPUT_FILENAME + ".mp3", 'rb')
        base64ToolContent = base64ToolFile.read()

        audio_64_encode = base64.encodebytes(base64ToolContent)
        os.remove(WAVE_OUTPUT_FILENAME)
        os.remove(WAVE_OUTPUT_FILENAME + ".mp3")
        return audio_64_encode.decode("utf-8")

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Record microphone' module records audio from the\n"
                                     "servers microphone if it's activated and listening.\n"
                                     "With the param '-t <secs>' you can specify how long."),
            'cmd': 'rm [-t <secs>]',
            'ext': self.pritify4log(
                   '-t\tSpecify how long the audio record will be (in seconds)\n\n'
                   f'Default record time is {RECORD_SECONDS} seconds.')
        }
        return help_txt
