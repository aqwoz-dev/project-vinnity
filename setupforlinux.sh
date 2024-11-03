#!/bin/bash

# Vinnity klasörünün bulunduğu yer
SOURCE_PATH="$(pwd)/vinnity"
DESTINATION_PATH="$HOME/.local/share/vinnity"

# Vinnity klasörünü kopyala
if [ -d "$SOURCE_PATH" ]; then
    mkdir -p "$DESTINATION_PATH"
    cp -r "$SOURCE_PATH"/* "$DESTINATION_PATH/"
    echo "Copied .vinnity to $DESTINATION_PATH."
else
    echo "Vinnity klasörü bulunamadı: $SOURCE_PATH"
    exit 1
fi

# PATH'e ekle
if ! grep -q "$DESTINATION_PATH" ~/.bashrc; then
    echo "export PATH=\"$DESTINATION_PATH:\$PATH\"" >> ~/.bashrc
    echo "$DESTINATION_PATH PATH'e eklendi."
else
    echo "$DESTINATION_PATH zaten PATH'te mevcut."
fi

echo "Setup is succeeded."
