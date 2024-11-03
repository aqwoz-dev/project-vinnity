import threading
import socket

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
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            print(f"Connection error: {e}")

    def send_message(self, message):
        """Send a message to the server."""
        if self.connected and self.socket:
            try:
                self.socket.sendall(f"{self.username}: {message}".encode('utf-8'))
            except Exception as e:
                print(f"Error sending message: {e}")

    def receive_messages(self):
        """Thread for receiving messages from the server."""
        while self.connected:
            try:
                response = self.socket.recv(1024)
                if response:
                    print(response.decode('utf-8'))
                else:
                    self.connected = False
                    print("Server connection lost.")
            except Exception as e:
                print(f"Error receiving message: {e}")
                self.connected = False

    def disconnect(self):
        """Disconnect from the server."""
        if self.socket:
            self.socket.close()
            self.connected = False
            print(f"{self.username} disconnected from the server.")

if __name__ == "__main__":
    username = input("Enter your username: ")
    host = input("Enter server address (e.g., localhost or IP): ")
    port = int(input("Enter server port (e.g., 12345): "))

    user = User(username)
    user.connect_to_server(host, port)

    while user.connected:
        message = input("Enter message to send (type 'exit' to quit): ")
        if message.lower() == 'exit':
            user.disconnect()
            break
        user.send_message(message)
