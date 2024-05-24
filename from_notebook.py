import tkinter as tk
from tkinter import scrolledtext
import nbformat
import markdown
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from io import StringIO
import sys

class NotebookViewer(tk.Tk):
    def __init__(self, notebook_path):
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

        # Chargement du notebook
        self.notebook = nbformat.read(notebook_path, as_version=4)

        # Dictionnaire pour l'espace de noms partagé
        self.namespace = {}

        for i, cell in enumerate(self.notebook.cells):
            if cell.cell_type == 'markdown':
                text = cell.source
                self.add_subframe(text)
            elif cell.cell_type == 'code':
                code = cell.source
                self.add_code_subframe(code)

        # Configurer le canevas pour ajuster sa taille en fonction du cadre interne
        self.main_frame.bind("<Configure>", self.on_frame_configure)

    def add_subframe(self, text):
        # Création d'une nouvelle sous-frame pour le texte markdown
        new_subframe = tk.Frame(self.main_frame, width=100, height=120)
        new_subframe.pack(pady=10)
        
        html_text = markdown.markdown(text)
        
        label = tk.Label(new_subframe, text=html_text, justify=tk.LEFT, wraplength=600)
        label.pack(fill=tk.BOTH, expand=True)

        # Ajout de la référence de la nouvelle sous-frame à la liste
        self.subframes.append(new_subframe)
    
    def add_code_subframe(self, code):
        # Création d'une nouvelle sous-frame avec une zone de texte et un bouton d'exécution
        new_subframe = tk.Frame(self.main_frame, bg="lightgrey", padx=10, pady=10)
        new_subframe.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        code_text = scrolledtext.ScrolledText(new_subframe, wrap=tk.WORD, height=5, width=120)
        code_text.pack(fill=tk.BOTH, expand=True)
        code_text.insert(tk.END, code)

        num_frame = len(self.subframes)
        
        execute_button = tk.Button(new_subframe, text="Exécuter", command=lambda: self.execute_code(code_text, num_frame))
        execute_button.pack(pady=5)

        # Widget de texte pour afficher la sortie
        output_text = scrolledtext.ScrolledText(new_subframe, wrap=tk.WORD, height=5, width=120)
        output_text.pack(fill=tk.BOTH, expand=True)

        # Ajout de la référence de la nouvelle sous-frame à la liste
        self.subframes.append((new_subframe, output_text))

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def execute_code(self, code_text, num_frame):
        code = code_text.get("1.0", tk.END)
        # Redirection de la sortie vers le widget de texte dans la sous-frame
        output_text = self.subframes[num_frame][1]
        output_text.delete("1.0", tk.END)  # Effacer la sortie précédente

        # Capture de la sortie standard
        stdout_backup = sys.stdout
        sys.stdout = StringIO()
        
        # Création d'une nouvelle figure Matplotlib
        plt.figure()

        try:
            # Utiliser la méthode exec pour exécuter le code dans un namespace partagé
            exec(code, self.namespace)
            
            # Récupérer la sortie standard capturée
            output_text.insert(tk.END, sys.stdout.getvalue())
            
            # Si un graphique a été créé, nous l'affichons dans la sous-frame
            if plt.get_fignums():
                figure = plt.gcf()
                canvas = FigureCanvasTkAgg(figure, master=self.subframes[num_frame][0])
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            output_text.insert(tk.END, "Une erreur s'est produite : " + str(e) + "\n")
        finally:
            # Restaurer la sortie standard
            sys.stdout = stdout_backup

if __name__ == "__main__":
    notebook_path = "TP.ipynb"
    app = NotebookViewer(notebook_path)
    app.mainloop()
