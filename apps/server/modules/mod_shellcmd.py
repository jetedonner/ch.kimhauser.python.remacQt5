import time
import subprocess
import os


from apps.server.modules.libs.mod_interface import mod_interface

EXIT_CMD = "exit"

class mod_shellcmd(mod_interface):

    cmd_short = "sh"
    cmd_long = "shellcmd"
    cmd_desc = "Shell command module"

    command = ""
    running = False

    def setup_mod(self):
        print(f'Module Setup (mod_shellcmd) called successfully!')
        pass

    def run_cmd(self, cmd="", param=""):
        self.running = True
        self.command = param
        answer = ""
        # if param == "":
        cond = True
        while cond:
            # cntrl-c to quit
            # cmd2send = input('$: ')
            if self.command == "":
                time.sleep(3)
                continue
            try:
                process = subprocess.Popen(param, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = process.communicate()
                answer = out.decode('utf-8')
            except subprocess.CalledProcessError:
                answer = f'Error sending command "{cmd} {param}" to shell!'
            if param != "":
                cond = False

        self.running = False
        return answer

    def run_mod(self, cmd="", param=""):
        answer = ""
        while True:
            # cntrl-c to quit
            cmd2send = cmd #input('$: ')
            try:
                args = cmd2send.split(' ')
                if args[0] == 'exit':
                    break
                elif len(args) == 1 and param != "":
                    cmd2send = param
                my_env = os.environ.copy()
                # my_env["PATH"] = "/usr/sbin:/sbin:" + my_env["PATH"]
                # subprocess.Popen(my_command, env=my_env)
                # subprocess.call([os.getenv('SHELL'), '-i', '-c', cmd2send])
                # answer = os.tcsetpgrp(0, os.getpgrp())
                process = subprocess.Popen(cmd2send, env=my_env, shell=True, executable="/bin/zsh", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = process.communicate()
                if err is not None and err != b"":
                    answer = err.decode("utf-8")
                else:
                    answer = out.decode('utf-8')
                return answer
                # print(answer)
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

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Shell Command' module return opens a shell\n"
                                     "session on the server, executes a command and\n"
                                     "returns the result. You can also open a persistent\n"
                                     "shell session and continue to execute commands until\n"
                                     "you send the exit command which terminates the session\n??"
                                     "and the module."),
            'cmd': f'{self.getCmdVariants4Help()} [<shell command>]',
            'ext': self.pritify4log(
                   'Per default the module opens a persistent shell session and\n'
                   'keeps the connection open. If you specify an argument to\n'
                   'the "sh" module only the command will be executed and\n'
                   'the result returned after that the connection will be closed.')
        }
        return help_txt