import subprocess


class runCommand():

    def run_command(self, command):
        out, err = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return (out + err).decode('utf-8')