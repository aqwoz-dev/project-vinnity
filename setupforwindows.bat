@echo off
setlocal

:: Hedef dizin tanımlamaları
set "SOURCE=C:\Program Files\vinnity\.vinnity\backend\vinnity.py"
set "DESTINATION=%LOCALAPPDATA%\Programs\vinnity\backend"

:: Hedef dizini oluştur
if not exist "%DESTINATION%" (
    mkdir "%DESTINATION%"
)

:: Dosyayı kopyala
if exist "%SOURCE%" (
    copy "%SOURCE%" "%DESTINATION%\"
    echo Kopyalama işlemi tamamlandı: %SOURCE% to %DESTINATION%
) else (
    echo Vinnity.py dosyası bulunamadı: %SOURCE%
    exit /b 1
)

:: PATH'e ekleme işlemi
setx PATH "%PATH%;%LOCALAPPDATA%\Programs\vinnity"
if errorlevel 1 (
    echo PATH'e eklerken hata oluştu.
) else (
    echo PATH'e başarıyla eklendi.
)

echo Setup tamamlandı.
pause
