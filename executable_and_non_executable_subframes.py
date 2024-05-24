import tkinter as tk
import sys
from tkinter import scrolledtext
import random

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sous-frames avec code exécutable et sortie")

        # Création d'un canevas dans la frame principale avec une barre de défilement
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Création d'un cadre dans le canevas pour contenir les sous-frames
        self.main_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.main_frame, anchor=tk.NW)

        # Liste pour stocker les références des sous-frames
        self.subframes = []

        # Bouton pour ajouter une nouvelle sous-frame
        add_button = tk.Button(self, text="Ajouter une sous-code-frame", command=self.add_code_subframe)
        add_button.pack(pady=10)
        
        add_button2 = tk.Button(self, text="Ajouter une sous-non-code-frame", command=self.add_subframe)
        add_button2.pack(pady=10)

        # Configurer le canevas pour ajuster sa taille en fonction du cadre interne
        self.main_frame.bind("<Configure>", self.on_frame_configure)

    def add_subframe(self):
        # Création d'une nouvelle sous-frame avec une couleur aléatoire
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        new_subframe = tk.Frame(self.main_frame, bg=color, width=100, height=100)
        new_subframe.pack(pady=10)

        # Ajout de la référence de la nouvelle sous-frame à la liste
        self.subframes.append(new_subframe)
    
    def add_code_subframe(self):
        # Création d'une nouvelle sous-frame avec une zone de texte et un bouton d'exécution
        new_subframe = tk.Frame(self.main_frame, bg="lightgrey", padx=10, pady=10)
        new_subframe.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        code_text = scrolledtext.ScrolledText(new_subframe, wrap=tk.WORD, height=5, width=120)
        code_text.pack(fill=tk.BOTH, expand=True)

        execute_button = tk.Button(new_subframe, text="Exécuter", command=lambda: self.execute_code(code_text,num_frame))
        execute_button.pack(pady=5)

        # Widget de texte pour afficher la sortie
        output_text = scrolledtext.ScrolledText(new_subframe, wrap=tk.WORD, height=5, width=120)
        output_text.pack(fill=tk.BOTH, expand=True)

        # Ajout de la référence de la nouvelle sous-frame à la liste
        num_frame = len(self.subframes)
        self.subframes.append((new_subframe, output_text))

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def execute_code(self, code_text, num_frame):
        code = code_text.get("1.0", tk.END)
        # Redirection de la sortie vers le widget de texte dans la sous-frame
        output_text = self.subframes[num_frame][1]#presque sur que c'est la
        output_text.delete("1.0", tk.END)  # Effacer la sortie précédente
        try:
            # Utiliser la méthode insert() pour écrire dans le widget ScrolledText
            exec(code, {"print": lambda *args: output_text.insert(tk.END, " ".join(map(str, args)) + "\n")})
        except Exception as e:
            output_text.insert(tk.END, "Une erreur s'est produite : " + str(e) + "\n")


if __name__ == "__main__":
    app = App()
    app.mainloop()
