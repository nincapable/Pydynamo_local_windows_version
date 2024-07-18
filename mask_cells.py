import nbformat

# Load the provided notebook
notebook_path = 'TP_Version_1_M.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = nbformat.read(f, as_version=4)

# Mask cells containing the specified comment
comment_to_mask = "### Case de Fonctionnement ###"
for cell in notebook['cells']:
    if cell['cell_type'] == 'code' and comment_to_mask.lower() in cell['source'].lower():
        if 'metadata' not in cell:
            cell['metadata'] = {}
        cell['metadata']['jupyter'] = {'source_hidden': True}

# Save the modified notebook
updated_notebook_path = 'TP_Version_1_Masked.ipynb'
with open(updated_notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(notebook, f)

print(f"Updated notebook saved as {updated_notebook_path}")
