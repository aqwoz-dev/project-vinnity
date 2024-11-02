# Temel imajı seçin
FROM python:3.11-slim

# Çalışma dizinini oluştur ve ayarla
WORKDIR /app

# Gerekli dosyaları çalışma dizinine kopyala
COPY . /app

# PATH'e çalışma dizinini ekle
ENV PATH="/app:${PATH}"

# Gerekli Python bağımlılıklarını yükle
RUN pip install --no-cache-dir -r requirements.txt

# /etc/hosts dosyasına giriş ekle
RUN echo "127.0.0.1 myserver.local" >> /etc/hosts

# Gerekli portu expose et
EXPOSE 12345

# Kurulum scriptini çalıştır
CMD ["python", "setup.py"]
