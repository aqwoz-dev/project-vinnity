import socket
import threading


class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        self.host = sock.getsockname()[0]  # Sunucunun hostunu al
        self.port = sock.getsockname()[1]  # Sunucunun portunu al
        sock.listen(5)
        print(f"Server running on {self.host}:{self.port}")

        while True:
            client_socket, client_address = sock.accept()
            print(f"Connection from {client_address}")
            client_socket.send(b"Welcome to the server!")
            client_socket.close()

    def set_custom_hostname(self, hostname):
        try:
            # Hostname'i IP'ye çevir ve ayarla
            self.host = socket.gethostbyname(hostname)
            print(f"Hostname set to {hostname} (IP: {self.host})")
        except socket.gaierror:
            print("Invalid hostname. Could not resolve to an IP address.")


# Örnek kullanım
if __name__ == "__main__":
    server = Server("0.0.0.0", 12345)

    # Kullanıcıdan hostname al ve ayarla
    custom_hostname = input("Enter a custom hostname: ")
    server.set_custom_hostname(custom_hostname)

    server.start()
