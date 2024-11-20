import threading
import socket
import logging

# Loglama ayarları
logging.basicConfig(
    filename='client.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class User:
    def __init__(self, user_name):
        self.username = user_name
        self.socket = None
        self.connected = False

    def connect_to_server(self, server_host, server_port):
        """Create a socket to connect to the server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((server_host, server_port))
            self.connected = True
            print(f"{self.username} connected to the server.")
            logging.info(f"{self.username} connected to the server at {server_host}:{server_port}.")
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            logging.error(f"Connection error: {e}")
            print(f"Connection error: {e}")

    def send_message(self, message):
        """Send a message to the server."""
        if self.connected and self.socket:
            try:
                self.socket.sendall(f"{self.username}: {message}".encode('utf-8'))
                logging.info(f"Message sent: {message}")
            except Exception as e:
                logging.error(f"Error sending message: {e}")
                print(f"Error sending message: {e}")
        else:
            print("You are not connected to the server.")

    def receive_messages(self):
        """Thread for receiving messages from the server."""
        while self.connected:
            try:
                response = self.socket.recv(1024)
                if response:
                    decoded_response = response.decode('utf-8')
                    print(decoded_response)
                    logging.info(f"Message received: {decoded_response}")
                else:
                    self.connected = False
                    print("Server connection lost.")
                    logging.warning("Server connection lost.")
            except Exception as e:
                logging.error(f"Error receiving message: {e}")
                print(f"Error receiving message: {e}")
                self.connected = False

    def disconnect(self):
        """Disconnect from the server."""
        if self.socket:
            try:
                self.socket.close()
                logging.info(f"{self.username} disconnected from the server.")
                print(f"{self.username} disconnected from the server.")
            except Exception as e:
                logging.error(f"Error while disconnecting: {e}")
                print(f"Error while disconnecting: {e}")
            finally:
                self.connected = False

if __name__ == "__main__":
    try:
        username = input("Enter your username: ").strip()
        if not username:
            print("Username cannot be empty.")
            exit(1)

        host = input("Enter server address (e.g., localhost or IP): ").strip()
        if not host:
            print("Server address cannot be empty.")
            exit(1)

        port_input = input("Enter server port (e.g., 12345): ").strip()
        try:
            port = int(port_input)
        except ValueError:
            print("Port must be a valid integer.")
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
        print("\nExiting client. Goodbye!")
        if user.connected:
            user.disconnect()
