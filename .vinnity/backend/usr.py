import os
import threading
import socket
import setup

class User:
    def __init__(self, username):
        self.username = username
        self.token = setup.token  # Token'in setup modülünden alınıyor
        self.socket = None  # Kullanıcıya ait socket
        self.connected = False  # Kullanıcının sunucu ile bağlantı durumu

    def connect_to_server(self, host, port):
        """Sunucuya bağlanmak için socket oluştur."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.connected = True
            print(f"{self.username} sunucuya bağlandı.")
        except Exception as e:
            print(f"Bağlantı hatası: {e}")

    def send_message(self, message):
        """Sunucuya mesaj göndermek için."""
        if self.connected and self.socket:
            try:
                self.socket.sendall(f"{self.username}: {message}".encode('utf-8'))
            except Exception as e:
                print(f"Mesaj gönderme hatası: {e}")

    def receive_messages(self):
        """Sunucudan gelen mesajları almak için bir thread."""
        while self.connected:
            try:
                response = self.socket.recv(1024)
                if response:
                    print(response.decode('utf-8'))
                else:
                    self.connected = False
                    print("Sunucu bağlantısı kesildi.")
            except Exception as e:
                print(f"Mesaj alma hatası: {e}")
                self.connected = False

    def disconnect(self):
        """Sunucudan ayrılmak için."""
        if self.socket:
            self.socket.close()
            self.connected = False
            print(f"{self.username} sunucudan ayrıldı.")
