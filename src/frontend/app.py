import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
import subprocess
import logging
import sys

# Loglama ayarları
logging.basicConfig(
    filename='vinnity_gui.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

server_process = None  # Global değişken


def start_server():
    """Sunucuyu başlat."""
    global server_process
    if server_process is not None and server_process.poll() is None:
        messagebox.showinfo("Sunucu", "Sunucu zaten çalışıyor!")
        return

    try:
        server_process = subprocess.Popen([sys.executable, 'server.py'])
        logging.info(f"Server started with PID: {server_process.pid}")
        messagebox.showinfo("Sunucu", f"Sunucu başlatıldı! PID: {server_process.pid}")
    except Exception as e:
        logging.error(f"Failed to start the server: {e}")
        messagebox.showerror("Hata", f"Sunucu başlatılamadı: {e}")


def stop_server():
    """Sunucuyu durdur."""
    global server_process
    if server_process is None or server_process.poll() is not None:
        messagebox.showinfo("Sunucu", "Sunucu zaten durdurulmuş!")
        return

    try:
        server_process.terminate()
        server_process.wait(timeout=5)
        logging.info("Server stopped.")
        messagebox.showinfo("Sunucu", "Sunucu durduruldu!")
        server_process = None
    except Exception as e:
        logging.error(f"Failed to stop the server: {e}")
        messagebox.showerror("Hata", f"Sunucu durdurulamadı: {e}")


def join_server():
    """Sunucuya bağlan."""
    ip_port = askstring("Sunucuya Katıl", "Bağlanılacak sunucuyu 'ip:port' formatında girin:")
    if not ip_port:
        return

    try:
        ip, port = ip_port.split(':')
        port = int(port)
        subprocess.Popen([sys.executable, 'user_client.py', ip, str(port)])
        logging.info(f"Client started for {ip}:{port}")
        messagebox.showinfo("Müşteri", f"Sunucuya bağlanıldı: {ip}:{port}")
    except ValueError:
        messagebox.showerror("Hata", "Geçersiz format. Doğru format: ip:port")
    except Exception as e:
        logging.error(f"Failed to join server: {e}")
        messagebox.showerror("Hata", f"Bağlanma hatası: {e}")


def show_messages():
    """Sunucu mesajlarını göster."""
    messagebox.showinfo("Mesajlar", "Bu özellik geliştirme aşamasında!")
    # İlgili kod burada genişletilebilir


# Tkinter arayüzü
root = tk.Tk()
root.title("Vinnity Yönetimi")
root.geometry("400x300")

# Logo
logo_label = tk.Label(root, text="VINNITY\nSunucu Yönetimi", font=("Arial", 16, "bold"))
logo_label.pack(pady=10)

# Butonlar
start_button = tk.Button(root, text="Sunucuyu Başlat", command=start_server, width=20, bg="green", fg="white")
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Sunucuyu Durdur", command=stop_server, width=20, bg="red", fg="white")
stop_button.pack(pady=5)

join_button = tk.Button(root, text="Sunucuya Katıl", command=join_server, width=20, bg="blue", fg="white")
join_button.pack(pady=5)

messages_button = tk.Button(root, text="Mesajları Göster", command=show_messages, width=20, bg="orange", fg="white")
messages_button.pack(pady=5)

# Çıkış
exit_button = tk.Button(root, text="Çıkış", command=root.quit, width=20, bg="black", fg="white")
exit_button.pack(pady=20)

root.mainloop()
