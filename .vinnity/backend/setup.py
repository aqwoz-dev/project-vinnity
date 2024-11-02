import platform
import subprocess

print("""
     _    ___             _ __           _____      __            
    | |  / (_)___  ____  (_) /___  __   / ___/___  / /___  ______ 
    | | / / / __ \/ __ \/ / __/ / / /   \__ \/ _ \/ __/ / / / __ \\
    | |/ / / / / / / / / / /_/ /_/ /   ___/ /  __/ /_/ /_/ / /_/ /
    |___/_/_/ /_/_/ /_/_/\__/\__, /   /____/\___/\__/\__,_/ .___/ 
                            /____/                       /_/      
""")

def detect_os():
    current_os = platform.system().lower()
    print(f"Detected operating system: {current_os}")
    return current_os

def is_docker_installed():
    try:
        # Docker'ın kurulu olup olmadığını kontrol et
        subprocess.run(["docker", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Docker is already installed.")
        return True
    except FileNotFoundError:
        print("Docker is not installed.")
        return False

def install_docker(os_name):
    try:
        if os_name == "linux":
            print("Installing Docker on Linux...")
            subprocess.run(["apt-get", "update"], check=True)
            subprocess.run(["apt-get", "install", "-y", "apt-transport-https", "ca-certificates", "curl", "software-properties-common"], check=True)
            # Add Docker GPG key
            subprocess.run(["curl", "-fsSL", "https://download.docker.com/linux/ubuntu/gpg"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["apt-key", "add", "-"], input=subprocess.PIPE)
            subprocess.run(["add-apt-repository", "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"], check=True)
            subprocess.run(["apt-get", "update"], check=True)
            subprocess.run(["apt-get", "install", "-y", "docker-ce"], check=True)
        elif os_name == "windows":
            print("Installing Docker on Windows...")
            subprocess.run(["powershell", "-Command", "Start-Process", "msiexec.exe", "-ArgumentList", "/i https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe /quiet /norestart", "-NoNewWindow", "-Wait"], check=True)
        elif os_name == "darwin":
            print("Installing Docker on macOS...")
            subprocess.run(["brew", "install", "docker"], check=True)
        else:
            print(f"Unknown operating system: {os_name}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing Docker: {e}")

def run_dockerfile():
    try:
        print("Building and running Docker container from Dockerfile...")
        # Docker imajı oluştur
        subprocess.run(["docker", "build", "-t", "my_docker_image", "."], check=True)
        # Docker konteynerini çalıştır
        subprocess.run(["docker", "run", "-d", "-p", "12345:12345", "my_docker_image"], check=True)
        print("Docker container is running.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Docker commands: {e}")

if __name__ == "__main__":
    os_name = detect_os()
    if not is_docker_installed():
        install_docker(os_name)
    run_dockerfile()
