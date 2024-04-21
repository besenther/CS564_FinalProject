import socket

SERVER_IP = '172.31.89.246'
SERVER_PORT = 8080

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
while True:
    server_socket.listen()

    print("Listening for connections...")

    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")

    while True:
        message = input("Enter command: ")
        conn.sendall(message.encode())

        response = conn.recv(1024)

        if not response:
            print("Connection to {} closed".format(addr[0]))
            break

        print("Received from client: ", response.decode())

print("Connection closed")