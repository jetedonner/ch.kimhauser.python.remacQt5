# from datetime import datetime
from apps.server.modules.libs.mod_interface import mod_interface
import argparse


class mod_args(mod_interface):

    cmd_short = "ar"
    cmd_long = "args"
    cmd_desc = "Args test module for processing module args"

    def setup_mod(self):
        print(f'Module Setup (mod_args) called successfully!')

    def run_mod(self, cmd="", param=""):
        print(f'Args Module')
        # now = datetime.now()
        # return f'Args module called @ {now.strftime("%m/%d/%Y, %H:%M:%S")}!'
        parser = argparse.ArgumentParser(prog=self.getCmdVariants4Help(), description=self.cmd_desc)
        parser.add_argument('integers', metavar='N', type=int, nargs='+',
                            help='an integer for the accumulator')
        parser.add_argument('--sum', dest='accumulate', action='store_const',
                            const=sum, default=max,
                            help='sum the integers (default: find the max)')

        # args = parser.parse_args(param.split(" "))
        # args = parser.parse_args()
        # print(args.accumulate(args.integers))
        return parser.format_help()

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Hello World' module just returns a string from\n"
                                     "the server to the client and acts as test function\n"
                                     "call to check the connection."),
            'cmd': f'{self.getCmdVariants4Help()}',
            'ext': 'This command has no arguments'
        }
        return help_txt
