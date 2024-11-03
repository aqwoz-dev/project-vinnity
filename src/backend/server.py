import socket
import threading
import logging

# Loglama ayarları
logging.basicConfig(
    filename='server.log',  # Log dosyası
    level=logging.INFO,  # Log seviyesini belirleme
    format='%(asctime)s - %(message)s'  # Log formatı
)

class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.clients = []

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(5)
        print(f"Server running on {self.host}:{self.port}")
        logging.info(f"Server running on {self.host}:{self.port}")

        while True:
            client_socket, client_address = sock.accept()
            print(f"Connection from {client_address}")
            logging.info(f"Connection from {client_address}")
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Received message: {message}")
                    logging.info(f"Received message: {message}")
                    self.broadcast(message, client_socket)
                else:
                    break
            except Exception as e:
                print(f"An error occurred: {e}")
                logging.error(f"An error occurred: {e}")
                break

        client_socket.close()
        self.clients.remove(client_socket)  # Bağlantıyı kapattıktan sonra istemciyi listeden çıkar

    def broadcast(self, message, client_socket):
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message.encode('utf-8'))
                except Exception as e:
                    print(f"Could not send message to a client: {e}")
                    logging.error(f"Could not send message to a client: {e}")

if __name__ == "__main__":
    server = Server("0.0.0.0", 12345)
    server.start()
