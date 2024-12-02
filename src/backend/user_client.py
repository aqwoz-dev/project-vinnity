import threading
import socket
import logging

# Loglama ayarları
logging.basicConfig(
    filename='client.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_and_print(message, level="info"):
    """Hem terminale hem de log dosyasına mesaj gönderir."""
    print(message)
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)

class User:
    def __init__(self, username):
        self.username = username
        self.socket = None
        self.connected = False

    def connect_to_server(self, server_host, server_port):
        """Create a socket to connect to the server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((server_host, server_port))
            self.connected = True
            log_and_print(f"{self.username} connected to the server at {server_host}:{server_port}.")
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            log_and_print(f"Connection error: {e}", "error")

    def send_message(self, message):
        """Send a message to the server."""
        if not self.connected:
            log_and_print("You are not connected to the server.", "warning")
            return
        try:
            self.socket.sendall(f"{self.username}: {message}".encode('utf-8'))
            logging.info(f"Message sent: {message}")
        except Exception as e:
            log_and_print(f"Error sending message: {e}", "error")

    def receive_messages(self):
        """Thread for receiving messages from the server."""
        while self.connected:
            try:
                response = self.socket.recv(1024)
                if response:
                    log_and_print(response.decode('utf-8'))
                else:
                    log_and_print("Server connection lost.", "warning")
                    self.disconnect()
            except Exception as e:
                log_and_print(f"Error receiving message: {e}", "error")
                self.disconnect()

    def disconnect(self):
        """Disconnect from the server."""
        if self.socket:
            try:
                self.socket.close()
            except Exception as e:
                log_and_print(f"Error while disconnecting: {e}", "error")
            finally:
                self.connected = False
                log_and_print(f"{self.username} disconnected from the server.")

if __name__ == "__main__":
    try:
        username = input("Enter your username: ").strip()
        if not username:
            log_and_print("Username cannot be empty.", "error")
            exit(1)

        host = input("Enter server address (e.g., localhost or IP): ").strip()
        if not host:
            log_and_print("Server address cannot be empty.", "error")
            exit(1)

        try:
            port = int(input("Enter server port (e.g., 12345): ").strip())
        except ValueError:
            log_and_print("Port must be a valid integer.", "error")
            exit(1)

        user = User(username)
        user.connect_to_server(host, port)

        while user.connected:
            message = input("Enter message to send (type 'exit' to quit): ").strip()
            if message.lower() == 'exit':
                user.disconnect()
                break
            elif message:
                user.send_message(message)
    except KeyboardInterrupt:
        log_and_print("\nExiting client. Goodbye!")
        if 'user' in locals() and user.connected:
            user.disconnect()
