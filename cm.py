import socket  
hostname = socket.gethostname()  
ip_address = socket.gethostbyname(hostname)  
print(f"IP-адрес {hostname}: {ip_address}")  

import os
name = os.getlogin()
print(name)
