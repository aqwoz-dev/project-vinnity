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
    filename='vinnity.log',  # Log dosyası
    level=logging.INFO,  # Log seviyesini belirleme
    format='%(asctime)s - %(message)s'  # Log formatı
)

logo = """
 _    ___             _ __           __  ___                                                  __ 
| |  / (_)___  ____  (_) /___  __   /  |/  /___ _____  ____ _____ ____  ____ ___  ___  ____  / /_
| | / / / __ \/ __ \/ / __/ / / /  / /|_/ / __ `/ __ \/ __ `/ __ `/ _ \/ __ `__ \/ _ \/ __ \/ __/
| |/ / / / / / / / / / /_/ /_/ /  / /  / / /_/ / / / / /_/ / /_/ /  __/ / / / / /  __/ / / / /_  
|___/_/_/ /_/_/ /_/_/\__/\__, /  /_/  /_/\__,_/_/ /_/\__,_/\__, /\___/_/ /_/ /_/\___/_/ /_/\__/  
                        /____/                            /____/                                 
"""

def start_server():
    """Sunucuyu başlat."""
    logging.info("Starting server...")
    server_process = subprocess.Popen([sys.executable, 'server.py'])
    return server_process

def stop_server(server_process):
    """Sunucuyu durdur."""
    if server_process:
        logging.info("Stopping server...")
        server_process.terminate()
        server_process.wait()  # Sunucunun durmasını bekle
        logging.info("Server stopped.")
    else:
        logging.warning("No server process to stop.")

def show_messages(host='localhost', port=12345):
    """Sunucudan mesajları göster."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            logging.info("Connected to the server to fetch messages.")

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

def start_client():
    """Müşteri uygulamasını başlat."""
    subprocess.Popen([sys.executable, 'client.py'])

def main():
    parser = argparse.ArgumentParser(description="All commands are there")
    parser.add_argument("-s", "--server", help="You should use it with a command.")
    parser.add_argument("-o", "--off", action='store_true', help="Turns off the server.")
    parser.add_argument("-O", "--on", action='store_true', help="Turns on the server.")
    parser.add_argument("-m", "--messages", action='store_true', help="Shows messages")
    parser.add_argument("-js", "--joinserver", help="Join the specified server.")

    # Argümanları al
    args = parser.parse_args()

    server_process = None

    if args.on:
        server_process = start_server()
    elif args.off:
        stop_server(server_process)
    elif args.messages:
        show_messages()  # Mesajları göster
    elif args.joinserver:
        start_client()  # Başka bir işlem olmadan doğrudan başlat
    else:
        print(logo)
        parser.print_help()

if __name__ == "__main__":
    main()
