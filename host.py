import socket

SERVER_IP = '172.31.23.98'
SERVER_PORT = 8080

# Discord bot stuff:
# get 1231711923532464240 MTIzMTcwOTU1MzU2NjAyNzg1OA.G3zTy9.DmP9aHL8EIYWLlOOGnTHD13-SPyBy3sziS3g_k

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

        response = conn.recv(4096)
        print(response.decode())

        if not response:
            print("Connection to {} closed".format(addr[0]))
            break

        while response.decode() != "Done":
            response = conn.recv(4096)
            print(response.decode())

print("Connection closed")