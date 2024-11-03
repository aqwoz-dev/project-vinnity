# Gerekli importlar
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
    filename='vinnity.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logo = """..."""  # Logo kodu burada kalabilir

# Küresel değişken
server_process = None

def start_server():
    """Sunucuyu başlat."""
    global server_process  # Küresel değişkeni kullan
    try:
        logging.info("Starting server...")
        server_process = subprocess.Popen([sys.executable, 'server.py'])
        return server_process
    except Exception as e:
        logging.error(f"Failed to start the server: {e}")
        print(f"Error: {e}")

def stop_server():
    """Sunucuyu durdur."""
    global server_process
    if server_process:
        try:
            logging.info("Stopping server...")
            server_process.terminate()
            server_process.wait()  # Sunucunun durmasını bekle
            logging.info("Server stopped.")
            server_process = None  # Sunucu durduğunda referansı sıfırla
        except Exception as e:
            logging.error(f"Failed to stop the server: {e}")
            print(f"Error: {e}")
    else:
        logging.warning("No server process to stop.")
