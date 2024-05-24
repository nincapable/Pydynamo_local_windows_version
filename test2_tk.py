import tkinter as tk
from tkinter import scrolledtext, ttk
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

class NotebookViewer(tk.Tk):
    def __init__(self, notebook_path):
        super().__init__()
        self.title("Notebook Viewer")

        # Création de la barre de défilement
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Création du cadre pour contenir les cellules
        self.cells_frame = tk.Frame(self)
        self.cells_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Lecture du notebook
        self.notebook = nbformat.read(notebook_path, as_version=4)
        self.code_cell_count = 0  # Compteur de cellules de code exécutées
        
        for i, cell in enumerate(self.notebook.cells):
            if cell.cell_type == 'markdown':
                text = cell.source
                self.display_markdown(text, row=i)
            elif cell.cell_type == 'code':
                code = cell.source
                self.create_code_cell(code)
        
        # Configurer la barre de défilement
        self.scrollbar.config(command=self.canvas.yview)

if __name__ == "__main__":
    notebook_path = "TP.ipynb"
    app = NotebookViewer(notebook_path)
    app.mainloop()