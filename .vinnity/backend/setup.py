import platform
import subprocess
import os

print("""\
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
        subprocess.run(["docker", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("Docker is already installed.")
        return True
    except FileNotFoundError:
        print("Docker is not installed.")
        return False


def install_docker(os_name):
    try:
        if os_name == "linux":
            print("Installing Docker on Linux...")
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "apt-transport-https", "ca-certificates", "curl",
                            "software-properties-common"], check=True)
            subprocess.run(
                ["curl", "-fsSL", "https://download.docker.com/linux/ubuntu/gpg", "|", "sudo", "apt-key", "add", "-"],
                shell=True, check=True)
            subprocess.run(["sudo", "add-apt-repository",
                            "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"],
                           check=True)
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "docker-ce"], check=True)
        elif os_name == "windows":
            print("Installing Docker on Windows...")
            subprocess.run(["powershell", "-Command", "Start-Process", "msiexec.exe", "-ArgumentList",
                            "/i https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe /quiet /norestart",
                            "-NoNewWindow", "-Wait"], check=True)
            print("Please restart your computer to complete the Docker installation.")
        elif os_name == "darwin":
            print("Installing Docker on macOS...")
            subprocess.run(["brew", "install", "docker"], check=True)
        else:
            print(f"Unknown operating system: {os_name}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing Docker: {e}")


def run_dockerfile(run_server):
    try:
        # İmaj adı belirleme
        image_name = "server_docker" if run_server else "normal_docker"

        print(f"Building Docker container from Dockerfile as {image_name}...")
        # Docker imajı oluştur
        subprocess.run(["docker", "build", "-t", image_name, "."], check=True)

        if run_server:
            print("Running Docker container with server...")
            # Docker konteynerini çalıştır
            subprocess.run(["docker", "run", "-d", "-p", "12345:12345", image_name], check=True)
            print("Docker container is running with server.")
        else:
            print("Docker container built but not running the server.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Docker commands: {e}")


if __name__ == "__main__":
    os_name = detect_os()
    if not is_docker_installed():
        install_docker(os_name)

    # Kullanıcıya sunucu kurmak isteyip istemediğini sor
    run_server_input = input("Do you want to run the server? (yes/no): ").strip().lower()
    while run_server_input not in ["yes", "no"]:
        run_server_input = input("Please answer with 'yes' or 'no': ").strip().lower()

    run_server = run_server_input == "yes"

    run_dockerfile(run_server)
