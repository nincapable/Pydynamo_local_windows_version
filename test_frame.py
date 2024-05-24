import tkinter as tk
import random

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Défilement vertical des sous-frames")

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
        add_button = tk.Button(self, text="Ajouter une sous-frame", command=self.add_subframe)
        add_button.pack(pady=10)

        # Configurer le canevas pour ajuster sa taille en fonction du cadre interne
        self.main_frame.bind("<Configure>", self.on_frame_configure)

    def add_subframe(self):
        # Création d'une nouvelle sous-frame avec une couleur aléatoire
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        new_subframe = tk.Frame(self.main_frame, bg=color, width=100, height=100)
        new_subframe.pack(pady=10)

        # Ajout de la référence de la nouvelle sous-frame à la liste
        self.subframes.append(new_subframe)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    app = App()
    app.mainloop()
