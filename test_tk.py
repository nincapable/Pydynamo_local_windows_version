import tkinter as tk
from tkinter import scrolledtext, ttk
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import markdown
from io import StringIO
import sys


class NotebookViewer(tk.Tk):
    def __init__(self, notebook_path):
        super().__init__()
        self.title("Notebook Viewer")

        # Création de la barre de défilement
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Création de la fenêtre défilante pour contenir le cadre de cellules
        self.canvas = tk.Canvas(self, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Création du cadre pour contenir les cellules
        self.cells_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.cells_frame, anchor=tk.NW)

        # Lecture du notebook
        self.notebook = nbformat.read(notebook_path, as_version=4)
        self.code_cell_count = 0  # Compteur de cellules de code exécutées

        # Affichage des cellules
        for i, cell in enumerate(self.notebook.cells):
            if cell.cell_type == 'markdown':
                text = cell.source
                self.display_markdown(text, row=i)
            elif cell.cell_type == 'code':
                code = cell.source
                self.create_code_cell(code)

        # Configurer la barre de défilement
        self.scrollbar.config(command=self.canvas.yview)

    def display_markdown(self, text, row):
        text_widget = scrolledtext.ScrolledText(self.cells_frame, wrap=tk.WORD, height=10, width=80)
        text_widget.insert(tk.END, text)
        text_widget.config(state=tk.DISABLED)
        text_widget.grid(row=row, column=0, padx=10, pady=10, columnspan=2)

    def create_code_cell(self, code):
        # Créer la zone de texte pour le code
        code_widget = scrolledtext.ScrolledText(self.cells_frame, wrap=tk.WORD, height=10, width=80)
        code_widget.insert(tk.END, code)
        code_widget.grid(row=self.code_cell_count, column=0, padx=10, pady=10)

        # Créer le bouton "Execute" pour exécuter le code
        execute_button = tk.Button(self.cells_frame, text="Execute", command=lambda widget=code_widget: self.execute_code(widget))
        execute_button.grid(row=self.code_cell_count, column=1, padx=10, pady=5)

        # Créer la zone de texte pour le résultat
        result_widget = tk.Text(self.cells_frame, wrap=tk.WORD, height=5, width=80)
        result_widget.grid(row=self.code_cell_count + 1, column=0, columnspan=2, padx=10, pady=5)

        self.code_cell_count += 2  # Incrémenter le compteur de cellules de code

        return code_widget, result_widget

    def execute_code(self, code_widget):
        code = code_widget.get("1.0", tk.END)
        execute_preprocessor = ExecutePreprocessor(timeout=-1, kernel_name='python3')
        code_to_execute = nbformat.v4.new_code_cell(code)

        try:
            executed_cell = execute_preprocessor.preprocess(code_to_execute, {'metadata': {'path': '.'}})[0]
            if executed_cell.get('outputs'):
                for output in executed_cell['outputs']:
                    if output.output_type == 'stream':
                        text = output.text.strip()
                        self.display_output(text)
        except Exception as e:
            print(e)
            return

        # Clear output and update code
        code_widget.delete("1.0", tk.END)
        code_widget.insert(tk.END, code_to_execute.source)

    def create_result_cell(self):
        result_label = tk.Label(self.cells_frame, text="")
        result_label.grid(row=self.code_cell_count, column=0, padx=10, pady=5, columnspan=2)

    def display_output(self, text):
        result_label = tk.Label(self.cells_frame, text=text)
        result_label.grid(row=self.code_cell_count, column=0, padx=10, pady=5, columnspan=2)

if __name__ == "__main__":
    notebook_path = "TP.ipynb"
    app = NotebookViewer(notebook_path)
    app.mainloop()
