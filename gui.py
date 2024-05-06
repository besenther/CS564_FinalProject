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


import threading as Recipe_App


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
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
        # self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        # self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        # self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        # self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=27, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=28, column=0, padx=20, pady=(10, 10))


        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=30, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
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
            label = customtkinter.CTkLabel(self, text=label_text, fg_color="transparent", font = ("Courier",30))
            label.grid(row=i, column=1, padx=(1, 1), pady=(1, 1), sticky="nsew")
            label.grid_forget()
            self.labels.append([label,label_text])
        self.count = 0
        self.ingredients = []

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

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
        except FileNotFoundError as e:
            print("Recipe Does not exist!!")

                    




if __name__ == "__main__":
    app = App()
    app.mainloop()