import tkinter
import tkinter.messagebox
import customtkinter
import json
import socket
import subprocess as validation_output
from subprocess import Popen as recipe_validator
import os as recipe_list
import discord as recipe_getter
import asyncio as recipe_generator
import random


import threading as Recipe_App


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"



units = ["mL","oz","in", "mi","km", "lbs", "g", "kg", "mg"]
seasonings = ["salt", "sugar", "thyme", "MSG", "curry powder", "garlic powder", "garam masala", "cilantro", "basil",
              "allspice", "ancho powder", "annatto seeds", "baharat seasoning", "basil", "bay leaves", "black pepper", "cardamom", "carom seeds", 
              "cayenne pepper", "celery seeds", "chervil", "chia seeds", "chicory", "chili powder", "chinese five-spice powder", "chipotle powder", 
              "chives", "cilantro", "cinnamon", "cloves", "coriander", "cumin", "curry leaves", "curry powder", "dill", "dukkah", "elderflower", "fenugreek", 
              "flax seeds", "garam masala", "garlic powder", "ginger", "gochugaru", "grains of paradise", "herbes de provence", "holy basil", "kaffir lime leaves", 
              "kosher salt", "lavender", "lemon basil", "lemongrass", "marjoram", "mustard seeds", "nutmeg", "oregano", "paprika", "parsley", "peppermint", "poppy seeds", 
              "rosemary", "saffron", "sage", "sesame seeds", "star anise", "sumac", "tarragon", "thyme", "turmeric", "vanilla", "wasabi", "white pepper", "zaatar", "ajwain", 
              "aleppo pepper", "asafoetida", "berbere", "caraway seeds", "cassia bark", "celery salt", "chervil", "cilantro seeds", "fennel seeds", "fenugreek leaves", "galangal", 
              "harissa", "juniper berries", "kala namak", "lemon pepper", "mace", "mahlab", "malabar pepper", "marash pepper", "nigella seeds", "old bay seasoning", "onion powder", "orange peel", 
              "orris root", "pandan leaf", "pasilla pepper", "pimento", "pink peppercorns", "ras el hanout", "red pepper flakes", "sichuan pepper", "spearmint", "sweet basil", "tamarind", "tonka bean", "umeboshi vinegar"]


ingredients = ["bacon", "pork", "beef", "carrots", "potatos", "chicken", "fish", "onions", "garlic",
               "artichoke", "asparagus", "bell pepper", "bok choy", "broccoli", "rapini", "brussels sprout", 
               "butternut squash", "cabbage", "red cabbage", "carrot", "cauliflower", "celery", "chives", "arugula",
                 "beet greens", "beets", "collard greens", "dandelion greens", "green onion", "eggplant", "endive", 
                 "garlic", "kale", "kimchi", "kohlrabi", "daikon", "spinach", "lettuce", "swiss chard", "cucumber", "peas", 
                 "beans", "lentils", "asparagus", "celery", "acorn squash", "alfalfa sprouts", "all blue potato", "amaranth", 
                 "ambercup squash", "anise", "avocado", "adzuki bean", "ahipa", "aonori", "arame", "arikara squash", "arrowroot", 
                 "asian greens", "azuki bean", "baby boo pumpkin", "bamboo shoot", "banana pepper", "banana squash", "basil", "bean sprout", 
                 "belgian endive", "bintje potato", "bitter melon", "black bean", "black-eyed pea", "black radish", "arrowhead elephant ear", "atibulnak", 
                 "beet (greens)", "binung", "borage greens", "broccoli (leaves / stalks)", "brooklime", "brussels sprouts", "cabbage", "caraway leaves", "catsear", 
                 "chickweed", "chicory", "chinese cabbage", "chinese mallow", "collard greens", "common purslane", "corn salad", "cress", "cucumis prophetarum", "garland chrysanthemum", 
                 "ground elder", "dill", "endive", "fat hen", "fiddlehead", "fluted pumpkin", "gnetum / melinjo", "golden samphire", "good king henry", "grape (leaves)", "greater plantain", 
                 "jute mallow / melokhia", "kale", "kalette", "kerguelen cabbage", "komatsuna","pork", "beef", "lamb and mutton", "chicken", "turkey", "venison", "duck", "wild boar", "goose", 
                 "rabbit", "pheasant", "goat meat", "bison", "salami", "ham", "bacon", "prosciutto", "sausages", "ground pork", "ground beef", "ground lamb", "ground chicken",
                   "ground turkey", "kangaroo", "ostrich", "elk", "quail", "emu", "alligator", "buffalo", "horse", "camel", "snail", "crab", "lobster", "octopus", "squid", "escargot (snails)", "frog legs", "turtle"]



temperatures = ["C", "F", "K"]

wet_ingredients = ["butter", "water", "chicken broth", "beef broth","milk", "water", "oil (such as vegetable oil, olive oil, or coconut oil)", "butter", "heavy cream",
                    "sour cream", "yogurt", "eggs", "honey", "maple syrup", "molasses", "vanilla extract", "lemon juice", "orange juice", "lime juice", "apple cider vinegar", 
                    "white vinegar", "red wine vinegar", "balsamic vinegar", "soy sauce", "fish sauce", "worcestershire sauce", "hot sauce", "tomato sauce", "ketchup", "mustard", 
                    "mayonnaise", "tahini", "pesto", "coconut milk", "almond milk", "chicken broth", "beef broth", "vegetable broth", "clam juice", "oyster sauce", "peanut butter", "nutella",
                      "whipped cream", "cream cheese", "greek yogurt", "condensed milk", "evaporated milk", "rice vinegar", "sesame oil", "miso paste", "tamarind paste", "pumpkin puree", "applesauce", "red curry paste"]

time_units = ["milliseconds", "seconds", "minutes", "hours", "days"]
cooking_vessel = ["pot", "pan", "shoe", "bowl", "french oven", "dutch oven", "waffle maker", "toaster"]


class App(customtkinter.CTk):
    def __init__(self, steps = []):
        super().__init__()
        # print(steps)

        # configure window
        self.title("Recipe Creator")
        self.geometry(f"{1920}x{1080}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3,4,5,6,7,8,9,10), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        for i in range(3,40):
            self.grid_rowconfigure((i), weight=1)


        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=400, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=40, sticky="nsew", columnspan=1)
        for row in range(0,40):
            self.sidebar_frame.grid_rowconfigure(row, weight=1)
        for col in range(0,2):
            self.sidebar_frame.grid_columnconfigure(col,weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Recipe Creator", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.recipe_name = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Enter Recipe Name here")
        self.recipe_name.grid(row=5, column=0, columnspan=1, sticky="nsew")

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event,text="Save Recipe")
        self.sidebar_button_1.grid(row=7, column=0)

        self.recipe_load_name = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Enter filename of recipe here")
        self.recipe_load_name.grid(row=9, column=0, columnspan=1, sticky="nsew")
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.load_recipe,text = "Load Recipe")
        self.sidebar_button_2.grid(row=11, column=0)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.reset_recipe,text = "Remove Recipe")
        self.sidebar_button_3.grid(row=13, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, command=self.create_random_recipe, text = "Randomize!")
        self.sidebar_button_4.grid(row=15, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=27, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=28, column=0, padx=20, pady=(10, 10))


        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=30, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["10%","80%", "90%", "100%", "110%", "120%","200%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=31, column=0, padx=20, pady=(10, 20))


        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter Ingredient Here")
        self.entry.grid(row=39, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),command=self.add_ingredient,text = "Add ingredient/step to list")
        self.main_button_1.grid(row=39, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.labels = []
        for i in range(30):
            label_text = "test"
            label = customtkinter.CTkLabel(self, text=label_text, fg_color="transparent", font = ("Courier",20))
            label.grid(row=i, column=1, padx=(1, 1), pady=(1, 1), sticky="nsew")
            label.grid_forget()
            self.labels.append([label,label_text])
        self.count = 0
        self.ingredients = []

        if len(steps) > 0:
            self.show_initial_recipe(steps)


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        
        recipe_name = "_".join(self.recipe_name.get().split(" ")) +".txt"

        try:
            with open(recipe_name,"x+") as w:
                for i in self.ingredients:
                    w.write(i+ "\n")
        except FileExistsError as e:
            with open(recipe_name,"w") as w:
                for i in self.ingredients:
                    w.write(i)
            

    def add_ingredient(self):
        if(self.count < len(self.labels)):
            self.labels[self.count][0].grid(row=self.count, column=1, padx=(1, 1), pady=(1, 1), sticky="nsew")
            self.labels[self.count][0].configure(text=self.entry.get())
            self.count +=1
            self.ingredients.append(self.entry.get())

    def load_recipe(self):
        self.reset_recipe()
        try:
            with open(self.recipe_load_name.get(),"r") as w:
                self.count = 0
                self.ingredients = []
                for line in w:
                    if self.count < len(self.labels):
                        self.labels[self.count][0].grid(row=self.count, column=1, padx=(1, 1), pady=(1, 1), sticky="nsew")
                        self.labels[self.count][0].configure(text=line)
                        self.count +=1
                        self.ingredients.append(line)
        except FileNotFoundError:
            pass
            # print("Recipe Does not exist!!")

    def show_initial_recipe(self,steps):
        self.count = 0
        for step in steps:
            if self.count < len(self.labels):
                    self.labels[self.count][0].grid(row=self.count, column=1, padx=(1, 1), pady=(1, 1), sticky="nsew")
                    self.labels[self.count][0].configure(text=step)
                    self.count +=1
                    self.ingredients.append(step)


    def reset_recipe(self):
        self.count = 0
        self.ingredients = []
        for i in range(30):
            self.labels[i][0].grid_forget()


    def create_random_recipe(self):
        self.reset_recipe()
        steps = self._make_random_recipe()
        self.show_initial_recipe(steps)



    def _make_random_recipe(self):
        steps = random.randint(0,25)
        commands = ["add", "mix in", "stir", "cook for", "wait"]
        all_steps = []

        for i in range(steps):
            typ = random.randint(0,4)
            command = commands[typ]

            if command ==  "add":
                ingredients_num = random.randint(1,2)
                step = f'add '

                for i in range(ingredients_num):
                    if i > 0:
                        step += "and "
                    amount = random.randint(0,100)
                    
                    step += f'{amount} {units[random.randint(0,len(units)-1)]} of {ingredients[random.randint(0,len(ingredients)-1)]} '
                all_steps.append(step)
                


            if command ==  "mix in":
                seasonings_num = random.randint(1,4)
                step = f'mix in '

                for i in range(seasonings_num):
                    if i > 0:
                        step += "and "
                    amount = random.randint(0,100)
                    
                    step += f'{amount} {units[random.randint(0,len(units)-1)]} of {seasonings[random.randint(0,len(seasonings)-1)]} '
                all_steps.append(step)


                pass


            if command ==  "stir":
                step = f'stir in '
                amount = random.randint(0,100)
                step += f'{amount} {units[random.randint(0,len(units)-1)]} of {wet_ingredients[random.randint(0,len(wet_ingredients)-1)]} '
                all_steps.append(step)
                pass

            if command ==  "wait":
                step = f'wait for '
                amount = random.randint(0,100)
                step += f'{amount} {time_units[random.randint(0,len(time_units)-1)]} '
                all_steps.append(step)

            
            if command ==  "cook for":
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
    app = App()
    app.mainloop()