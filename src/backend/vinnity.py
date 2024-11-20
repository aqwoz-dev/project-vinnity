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

server_process = None  # Global değişken olarak tanımlandı

def start_server():
    """Sunucuyu başlat."""
    global server_process
    if server_process is not None and server_process.poll() is None:
        logging.warning("Server is already running.")
        print("Server is already running.")
        return server_process

    try:
        logging.info("Starting server...")
        server_process = subprocess.Popen([sys.executable, 'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"Server started with PID: {server_process.pid}")
        print(f"Server started with PID: {server_process.pid}")
        return server_process
    except Exception as e:
        logging.error(f"Failed to start the server: {e}")
        print(f"Error: {e}")

def stop_server():
    """Sunucuyu durdur."""
    global server_process
    if server_process is not None:
        if server_process.poll() is None:  # Sürecin hala çalışıp çalışmadığını kontrol et
            try:
                logging.info("Stopping server...")
                server_process.terminate()
                server_process.wait(timeout=5)
                logging.info("Server stopped.")
                print("Server stopped.")
                server_process = None
            except subprocess.TimeoutExpired:
                logging.warning("Server did not stop in time. Forcing termination.")
                server_process.kill()
                logging.info("Server process killed.")
                print("Server process killed.")
                server_process = None
            except Exception as e:
                logging.error(f"Failed to stop the server: {e}")
                print(f"Error: {e}")
        else:
            logging.warning("Server is already stopped.")
            print("Server is already stopped.")
            server_process = None
    else:
        logging.warning("No server process to stop.")
        print("No server process to stop.")

def show_messages(host='localhost', port=12345):
    """Sunucudan mesajları göster."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            logging.info("Connected to the server to fetch messages.")
            print("Connected to the server to fetch messages.")

            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Message from server: {message}")
                    logging.info(f"Message from server: {message}")
                else:
                    break
    except Exception as e:
        logging.error(f"Error connecting to the server: {e}")
        print(f"Error: {e}")

def start_client(ip_address, port):
    """Müşteri uygulamasını başlat."""
    try:
        subprocess.Popen([sys.executable, 'user_client.py', ip_address, str(port)])
        logging.info(f"Client started for {ip_address}:{port}")
        print(f"Client started for {ip_address}:{port}")
    except Exception as e:
        logging.error(f"Failed to start the client: {e}")
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Vinnity Server Management")
    parser.add_argument("-o", "--off", action='store_true', help="Turns off the server.")
    parser.add_argument("-O", "--on", action='store_true', help="Turns on the server.")
    parser.add_argument("-m", "--messages", action='store_true', help="Shows messages from the server.")
    parser.add_argument("-js", "--joinserver", help="Join the specified server in the format 'ip:port'.")

    args = parser.parse_args()

    if args.on:
        start_server()
    elif args.off:
        stop_server()
    elif args.messages:
        show_messages()  # Mesajları göster
    elif args.joinserver:
        try:
            ip, port = args.joinserver.split(':')
            port = int(port)
            start_client(ip, port)
        except ValueError:
            logging.error("Invalid joinserver format. Use 'ip:port'.")
            print("Error: Invalid joinserver format. Use 'ip:port'.")
    else:
        print(logo)
        parser.print_help()

if __name__ == "__main__":
    main()
