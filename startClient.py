import sys

from apps.client.reMac_client import reMac_client


class ReMacClientCli:

    myReMacClient = reMac_client()

    def main(self):
        if len(sys.argv) >= 3:
            self.myReMacClient.start_client(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


if __name__ == "__main__":
    ReMacClientCli().main()
