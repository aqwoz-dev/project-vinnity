import socket
import threading
import logging

# Loglama ayarları
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = None
        self.running = True

    def log_error(self, message):
        """Hataları loglamak için yardımcı fonksiyon."""
        print(message)
        logging.error(message)

    def run(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)  # Dinleme kuyruğu artırıldı
        print(f"Server running on {self.host}:{self.port}")
        logging.info(f"Server running on {self.host}:{self.port}")

        try:
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"Connection from {client_address}")
                    logging.info(f"Connection from {client_address}")
                    self.clients.append(client_socket)
                    threading.Thread(target=self.handle_client, args=(client_socket,)).start()
                except Exception as e:
                    self.log_error(f"Error while accepting connection: {e}")
        except KeyboardInterrupt:
            print("\nShutting down server...")
            self.shutdown()

    def handle_client(self, client_socket):
        try:
            while self.running:
                try:
                    message = client_socket.recv(1024).decode('utf-8')
                    if message:
                        print(f"Received message: {message}")
                        logging.info(f"Received message: {message}")
                        self.broadcast(message, client_socket)
                    else:
                        break  # Bağlantı kapandığında döngüyü kır
                except Exception as e:
                    self.log_error(f"Error receiving message: {e}")
                    break
        finally:
            self.remove_client(client_socket)

    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except Exception as e:
                    self.log_error(f"Failed to send message: {e}")
                    self.remove_client(client)

    def remove_client(self, client_socket):
        if client_socket in self.clients:
            self.clients.remove(client_socket)
            try:
                client_socket.close()
                print(f"Disconnected client: {client_socket.getpeername()}")
                logging.info(f"Disconnected client: {client_socket.getpeername()}")
            except Exception as e:
                self.log_error(f"Error closing client socket: {e}")

    def shutdown(self):
        """Sunucuyu kapatır ve tüm istemcileri temizler."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        for client in self.clients:
            try:
                client.close()
            except Exception as e:
                self.log_error(f"Error closing client socket: {e}")
        print("Server shut down.")
        logging.info("Server shut down.")

if __name__ == "__main__":
    host_ip = socket.gethostbyname(socket.gethostname())
    port = 12345

    server = Server(host_ip, port)
    server.start()
