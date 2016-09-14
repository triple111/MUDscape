from socketserver import TCPServer, BaseRequestHandler
import signal
import sys
from colorama import init, Fore, Back, Style
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .commands import commands
from .models import *
from .exceptions import LogoutException
from .screens import *
from .constants import *


class MUDHandler(BaseRequestHandler):
    #track number of connections statically:
    connectionCount = 0

    def handle(self):
        print(self.client_address[0], 'connected')

        # Connect to the database
        self.conn = sessionmaker(bind=Base.metadata.bind)()
        self.authenticated = False
        self.prompt = "{RED}> {RESET}"

        MUDHandler.connectionCount += 1
        # Start user input
        self.send(welcomeMessage(MUDHandler.connectionCount))
        self.loop()

    def loop(self):
        while True:
            data = self.require_input()

            try:
                command, *args = data.split()

                # Command handling
                try:
                    if not self.authenticated:
                        if command == 'login':
                            commands['login'].perform(self, *args)
                            continue

                        elif command == 'quit':
                            commands['quit'].perform(self, *args)
                            continue

                        else:
                            self.send('{YELLOW}You must log in first. Type "login"')
                            continue

                    message = commands[command].perform(self, *args)
                    self.send(message)
                except KeyError:  # No such command
                    self.send('{YELLOW}Invalid command!{RESET}')
                except TypeError:  # Syntax error
                    message = commands[command].help()
                    self.send(message)
                except LogoutException:  # User to be disconnected
                    MUDHandler.connectionCount -= 1
                    break

            except ValueError:  # Client sends empty command
                self.send()

    def require_input(self, message=None, echoOutput=False):
        """Repeatedly prompt user for input until something is provided"""
        data = bytes()

        while len(data) == 0:
            if message:
                self.send(message)
            data = self.bufferInput().strip().decode('utf-8').lower()

        logMessage = str(self.client_address[0]) + "input: " + str(data)

        #print input attempt to server console
        if echoOutput:
            if data is not None:
                print(logMessage)

        return data

    def send(self, message='', prompt=True):
        if prompt:
            # Add prompt if specified
            message = '{}\n{}'.format(message, self.prompt)
        else:
            message = '{}\n'.format(message)

        self.request.sendall(message.format(**Fore.__dict__).encode('utf-8'))

    def bufferInput(self):
        data = bytearray()

        while True:
            inputBytes = iter(self.request.recv(1024))

            for byte in inputBytes:
                #check if byte is a telnet command
                if byte in TELNET.values():
                    #if next byte is a telnet command that expects an argument, skip the argument
                    if byte in (TELNET['WILL'], TELNET['WONT'], TELNET['DO'], TELNET['DONT']):
                        next(inputBytes)
                    #skip the IAC
                    continue
                #if a new line is encountered, terminate parsing and return the completed command
                elif byte in (ASCII['NEW_LINE'], ASCII['RETURN']):
                    return data

                #TODO add special character processing (like delete and backspace)
                elif byte in (ASCII['BACKSPACE'], ASCII['DELETE']):
                    continue

                data.append(byte)

            #ensure an infinite loop does not occur if input is solely telnet commands
            if len(data) == 0:
                break
        return data

def start_db():
    engine = create_engine('sqlite:///mudscape.sqlite')

    # Create all tables in db
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine


def main():
    HOST, PORT = "localhost", 8001
    server = TCPServer((HOST, PORT), MUDHandler)

    init()  # colorama
    start_db()

    print('Starting server at {}:{}'.format(HOST, PORT))

    server.serve_forever()


def sigint_handler(signal, frame):
    print('Shutting down')
    sys.exit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)
    main()
