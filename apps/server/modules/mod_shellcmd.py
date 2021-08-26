import os
import subprocess

from apps.server.modules.libs.mod_interface import mod_interface

EXIT_CMD = "exit"

class mod_shellcmd(mod_interface):


    def setup_mod(self):
        print(f'Module Setup (mod_shellcmd) called successfully!')
        pass

    def run_cmd(self, cmd = "", param = ""):
        answer = ""
        # while True:
        # cntrl-c to quit
        # cmd2send = input('$: ')
        try:
            # args = cmd2send.split(' ')
            # if cmd == 'exit':
            #     break
            process = subprocess.Popen(param, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            answer = out.decode('utf-8')
            print(answer)
        except subprocess.CalledProcessError:
            answer = f'Error sending command "{cmd} {param}" to shell!'
        return answer

    def run_mod(self, cmd = ""):
        answer = ""
        while True:
            # cntrl-c to quit
            cmd2send = input('$: ')
            try:
                args = cmd2send.split(' ')
                if args[0] == 'exit':
                    break
                process = subprocess.Popen(cmd2send, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = process.communicate()
                answer = out.decode('utf-8')
                print(answer)
            except subprocess.CalledProcessError:
                answer = f'Error sending command "{cmd2send}" to shell!'
            # print(err)
        # while True:
        #     cmd2send = input("$:")
        #     #print(f'Sending command: "{cmd2send}" to shell ...')
        #     try:
        #         args = cmd2send.split(" ")
        #         if args[0] == EXIT_CMD:
        #             break
        #         answer = subprocess.check_output(cmd2send, shell=True)
        #         print(answer.decode("utf-8"))
        #     except subprocess.CalledProcessError:
        #         answer = f'Error sending comand "{cmd2send}" to shell!'
        return answer
