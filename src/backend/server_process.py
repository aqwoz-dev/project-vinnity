import os
import sys
import subprocess
import logging
import argparse

# Loglama ayarları
logging.basicConfig(
    filename='vinnity.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logo = """
____   ____.__              .__  __          
\   \ /   /|__| ____   ____ |__|/  |_ ___.__.
 \   Y   / |  |/    \ /    \|  \   __<   |  |
  \     /  |  |   |  \   |  \  ||  |  \___  |
   \___/   |__|___|  /___|  /__||__|  / ____|
                   \/     \/          \/     
"""

PID_FILE = 'server.pid'


def save_pid(pid):
    """Sunucu PID'sini kaydeder."""
    with open(PID_FILE, 'w') as f:
        f.write(str(pid))


def get_saved_pid():
    """Kaydedilen PID'yi okur."""
    if os.path.exists(PID_FILE):
        with open(PID_FILE, 'r') as f:
            return int(f.read())
    return None


def start_server():
    """Sunucuyu başlatır."""
    server_script = os.path.join(os.getcwd(), 'server.py')
    if not os.path.exists(server_script):
        logging.error(f"Server script not found: {server_script}")
        print(f"Error: 'server.py' not found in the current directory.")
        return None

    try:
        logging.info("Starting server...")
        process = subprocess.Popen([sys.executable, server_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        save_pid(process.pid)
        logging.info(f"Server process started with PID: {process.pid}")
        return process
    except Exception as e:
        logging.error(f"Failed to start the server: {e}")
        print(f"Error starting server: {e}")
        return None


def stop_server():
    """Sunucuyu durdurur."""
    pid = get_saved_pid()
    if pid is None:
        logging.warning("No server process found to stop.")
        print("No server process is currently running.")
        return

    try:
        logging.info(f"Stopping server process with PID: {pid}")
        process = subprocess.Popen(['kill', str(pid)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate()  # Sunucu işlemi sonlandırılır
        logging.info("Server stopped successfully.")
        print("Server stopped successfully.")
    except Exception as e:
        logging.error(f"Failed to stop the server: {e}")
        print(f"Error stopping server: {e}")


def main():
    """Ana komut çalıştırıcı fonksiyon."""
    parser = argparse.ArgumentParser(description="Server control script.")
    parser.add_argument('action', choices=['start', 'stop'], help="Action to perform: start or stop the server.")
    args = parser.parse_args()

    if args.action == 'start':
        process = start_server()
        if process:
            print("Server is running. Press Ctrl+C to stop.")
            try:
                process.wait()  # Sunucunun arka planda çalışmasını sağlar
            except KeyboardInterrupt:
                stop_server()
    elif args.action == 'stop':
        stop_server()


if __name__ == "__main__":
    print(logo)
    main()
