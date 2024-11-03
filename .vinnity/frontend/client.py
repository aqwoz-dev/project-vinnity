#client.py
import socket
import threading

class Client:
    def __init__(self, host, port):
        self.server_address = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect(self.server_address)
        print("Connected to the server.")
        threading.Thread(target=self.receive_messages).start()

    def send_message(self, message):
        self.client_socket.send(message.encode('utf-8'))

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Received: {message}")
                else:
                    break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

        self.client_socket.close()

if __name__ == "__main__":
    host = input("Enter server host (e.g., localhost): ")
    port = int(input("Enter server port (e.g., 12345): "))

    client = Client(host, port)
    client.connect()

    while True:
        message = input("Enter message to send (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        client.send_message(message)

    client.client_socket.close()
