# server_progress.py
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

logo = f"""

____   ____.__              .__  __          
\   \ /   /|__| ____   ____ |__|/  |_ ___.__.
 \   Y   / |  |/    \ /    \|  \   __<   |  |
  \     /  |  |   |  \   |  \  ||  |  \___  |
   \___/   |__|___|  /___|  /__||__|  / ____|
                   \/     \/          \/     

"""

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
        logging.info(f"Server process started with PID: {process.pid}")
        return process
    except Exception as e:
        logging.error(f"Failed to start the server: {e}")
        print(f"Error starting server: {e}")
        return None

def stop_server(process):
    """Sunucuyu durdurur."""
    if process is None:
        logging.warning("No server process to stop.")
        print("No server process is currently running.")
        return

    try:
        logging.info(f"Stopping server process with PID: {process.pid}")
        process.terminate()
        process.wait(timeout=5)  # Sunucunun kapanması için 5 saniye bekle
        if process.poll() is not None:  # İşlem durdu mu kontrol et
            logging.info("Server stopped successfully.")
            print("Server stopped successfully.")
        else:
            logging.warning("Server did not stop within the timeout.")
            print("Server did not stop in the expected time.")
    except Exception as e:
        logging.error(f"Failed to stop the server: {e}")
        print(f"Error stopping server: {e}")

def main():
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
                stop_server(process)
    elif args.action == 'stop':
        # Daha önce başlatılan sunucuyu bulmak için process yönetimi eklenebilir.
        print("Server stop functionality needs additional implementation.")

if __name__ == "__main__":
    print(logo)
    main()
