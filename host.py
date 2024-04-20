import socket

SERVER_IP = '127.0.0.1'  # localhost
SERVER_PORT = 65432

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to the address and port
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # Listen for incoming connections
    server_socket.listen()

    print("Server is listening for incoming connections...")

    # Accept a connection from a client
    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")

    # Receive data from the client
    while True:
        # Send data to the server
        message = input("Enter command: ")
        conn.sendall(message.encode())

        # Receive a response from the server
        response = conn.recv(1024)
        print("Received from client: ", response.decode())

print("Connection closed")