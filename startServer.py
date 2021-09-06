import sys

from apps.server.reMac_server import reMac_server


class ReMacServerCli:

    myReMacServer = reMac_server()

    def main(self):
        if len(sys.argv) >= 3:
            self.myReMacServer.start_server(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    ReMacServerCli().main()
