import subprocess
import socket

def ssh_tunnel():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('127.0.0.1', 11434)) != 0:
            subprocess.run(["ssh", "-f", "-N", "mzaiam"])
            print("Tunnel just connected.")
        else:
            print("Tunnel connected.")