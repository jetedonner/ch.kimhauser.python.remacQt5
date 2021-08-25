import pyaudio
import wave
import base64
import os

from apps.server.modules.libs.mod_interfaceRunCmd import mod_interfaceRunCmd

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "output123.wav"


class mod_recmic(mod_interfaceRunCmd):
    def setup_mod(self):
        print(f'Module Setup (mod_recmic) called successfully!')

    def run_mod(self, cmd = ""):
        print(f'mod_recmic Module')

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

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
