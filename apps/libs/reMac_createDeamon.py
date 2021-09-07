import os

from PyQt5.QtCore import QFile, QTextStream


class reMac_createDeamon():

    def __init__(self):
        pass

    def createDeamon(self, key, program):
        ld_key = key
        ld_program = program

        f = QFile("res/templates/plist.xml")
        f.open(QFile.ReadOnly | QFile.Text)
        istream = QTextStream(f)
        xmlTxt = istream.readAll()
        xmlTxt = f"{xmlTxt}".format(**locals())
        xmlTxtOutput = f"Creating PLIST file with content:\n\n{xmlTxt}"
        f.close()
        cur_dir = os.path.abspath(f"./tmp")
        plistFile = f"{ld_key}.plist"
        sc_out = f"{cur_dir}/{plistFile}"
        print("sc_out: " + sc_out)
        xmlTxtOutput = xmlTxtOutput + f"\n\n> Writing PLIST file @: {sc_out}"
        print(xmlTxtOutput)

        with open(sc_out, "wb") as output_file:
            output_file.write(xmlTxt.encode())
            output_file.close()
        return [xmlTxtOutput, sc_out]
