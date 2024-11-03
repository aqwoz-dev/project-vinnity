#!/usr/bin/env python
# vinnity.py
# Management and main file
import os
import sys
import subprocess
import logging
import argparse
import socket
import user_client
import server

# Loglama ayarları
logging.basicConfig(
    filename='vinnity.log',  # Log dosyası
    level=logging.INFO,  # Log seviyesini belirleme
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log formatı
)

logo = """
 _    ___             _ __           __  ___                                                  __ 
| |  / (_)___  ____  (_) /___  __   /  |/  /___ _____  ____ _____ ____  ____ ___  ___  ____  / /_
| | / / / __ \/ __ \/ / __/ / / /  / /|_/ / __ `/ __ \/ __ `/ __ `/ _ \/ __ `__ \/ _ \/ __ \/ __/
| |/ / / / / / / / / / /_/ /_/ /  / /  / / /_/ / / / / /_/ / /_/ /  __/ / / / / /  __/ / / / /_  
|___/_/_/ /_/_/ /_/_/\__/\__, /  /_/  /_/\__,_/_/ /_/\__,_/\__, /\___/_/ /_/ /_/\___/_/ /_/\__/  
                        /____/                            /____/                                 
"""

server_process = None  # Global değişken olarak tanımlandı

def start_server():
    """Sunucuyu başlat."""
    global server_process  # Global değişkeni kullan
    try:
        logging.info("Starting server...")
        server_process = subprocess.Popen([sys.executable, 'server.py'])
        return server_process
    except Exception as e:
        logging.error(f"Failed to start the server: {e}")
        print(f"Error: {e}")

def stop_server():
    """Sunucuyu durdur."""
    global server_process  # Global değişkeni kullan
    if server_process:
        try:
            logging.info("Stopping server...")
            server_process.terminate()
            server_process.wait()  # Sunucunun durmasını bekle
            logging.info("Server stopped.")
            server_process = None  # Sunucu durduğunda process'i sıfırla
        except Exception as e:
            logging.error(f"Failed to stop the server: {e}")
            print(f"Error: {e}")
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

def start_client(ip_address, port):
    """Müşteri uygulamasını başlat."""
    try:
        subprocess.Popen([sys.executable, 'user_client.py', ip_address, str(port)])
    except Exception as e:
        logging.error(f"Failed to start the client: {e}")
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="All commands are there")
    parser.add_argument("-o", "--off", action='store_true', help="Turns off the server.")
    parser.add_argument("-O", "--on", action='store_true', help="Turns on the server.")
    parser.add_argument("-m", "--messages", action='store_true', help="Shows messages")
    parser.add_argument("-js", "--joinserver", help="Join the specified server in the format 'ip:port'.")

    # Argümanları al
    args = parser.parse_args()

    if args.on:
        if not server_process:  # Sunucu zaten çalışmıyorsa başlat
            start_server()
        else:
            logging.warning("Server is already running.")
    elif args.off:
        stop_server()
    elif args.messages:
        show_messages()  # Mesajları göster
    elif args.joinserver:
        # IP ve portu ayır
        try:
            ip, port = args.joinserver.split(':')
            port = int(port)  # Portu tam sayıya çevir
            start_client(ip, port)  # IP ve port ile client başlat
        except ValueError:
            logging.error("Invalid joinserver format. Use 'ip:port'.")
            print("Error: Invalid joinserver format. Use 'ip:port'.")
    else:
        print(logo)
        parser.print_help()

if __name__ == "__main__":
    main()

