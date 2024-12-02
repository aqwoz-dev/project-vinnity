#!/usr/bin/env python
# vinnity.py
# Management and main file

import os
import sys
import subprocess
import logging
import argparse
import socket

# Loglama ayarları
logging.basicConfig(
    filename='vinnity.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logo = r"""
 _    ___             _ __           __  ___                                                  __ 
| |  / (_)___  ____  (_) /___  __   /  |/  /___ _____  ____ _____ ____  ____ ___  ___  ____  / /_
| | / / / __ \/ __ \/ / __/ / / /  / /|_/ / __ `/ __ \/ __ `/ __ `/ _ \/ __ `__ \/ _ \/ __ \/ __/
| |/ / / / / / / / / / /_/ /_/ /  / /  / / /_/ / / / / /_/ / /_/ /  __/ / / / / / /  __/ / / / /_  
|___/_/_/ /_/_/ /_/_/\__/\__, /  /_/  /_/\__,_/_/ /_/\__,_/\__, /\___/_/ /_/ /_/\___/_/ /_/\__/  
                        /____/                            /____/                                 
"""

class ServerManager:
    def __init__(self):
        self.server_process = None

    def log_and_print(self, message):
        """Log and print a message."""
        print(message)
        logging.info(message)

    def start_server(self):
        """Start the server."""
        if self.server_process is not None and self.server_process.poll() is None:
            self.log_and_print("Server is already running.")
            return self.server_process

        try:
            self.log_and_print("Starting server...")
            self.server_process = subprocess.Popen(
                [sys.executable, 'server.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.log_and_print(f"Server started with PID: {self.server_process.pid}")
            return self.server_process
        except Exception as e:
            self.log_and_print(f"Failed to start the server: {e}")

    def stop_server(self):
        """Stop the server."""
        if self.server_process is not None:
            if self.server_process.poll() is None:  # Check if the process is still running
                try:
                    self.log_and_print("Stopping server...")
                    self.server_process.terminate()
                    self.server_process.wait(timeout=5)
                    self.log_and_print("Server stopped.")
                    self.server_process = None
                except subprocess.TimeoutExpired:
                    self.log_and_print("Server did not stop in time. Forcing termination.")
                    self.server_process.kill()
                    self.log_and_print("Server process killed.")
                    self.server_process = None
                except Exception as e:
                    self.log_and_print(f"Failed to stop the server: {e}")
            else:
                self.log_and_print("Server is already stopped.")
                self.server_process = None
        else:
            self.log_and_print("No server process to stop.")

    def show_messages(self, host='localhost', port=12345):
        """Show messages from the server."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((host, port))
                self.log_and_print("Connected to the server to fetch messages.")

                while True:
                    message = client_socket.recv(1024).decode('utf-8')
                    if message:
                        self.log_and_print(f"Message from server: {message}")
                    else:
                        break
        except Exception as e:
            self.log_and_print(f"Error connecting to the server: {e}")

    def start_client(self, ip_address, port):
        """Start the client application."""
        try:
            subprocess.Popen([sys.executable, 'user_client.py', ip_address, str(port)])
            self.log_and_print(f"Client started for {ip_address}:{port}")
        except Exception as e:
            self.log_and_print(f"Failed to start the client: {e}")

def main():
    parser = argparse.ArgumentParser(description="Vinnity Server Management")
    parser.add_argument("-o", "--off", action='store_true', help="Turns off the server.")
    parser.add_argument("-O", "--on", action='store_true', help="Turns on the server.")
    parser.add_argument("-m", "--messages", action='store_true', help="Shows messages from the server.")
    parser.add_argument("-js", "--joinserver", help="Join the specified server in the format 'ip:port'.")

    args = parser.parse_args()
    manager = ServerManager()

    if args.on:
        manager.start_server()
    elif args.off:
        manager.stop_server()
    elif args.messages:
        manager.show_messages()  # Show messages
    elif args.joinserver:
        try:
            ip, port = args.joinserver.split(':')
            port = int(port)
            manager.start_client(ip, port)
        except ValueError:
            manager.log_and_print("Invalid joinserver format. Use 'ip:port'.")
    else:
        print(logo)
        parser.print_help()

if __name__ == "__main__":
    main()