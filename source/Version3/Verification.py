import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import subprocess

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
    if file_path:
        show_certificate(file_path)

def show_certificate(file_path):
    try:
        result = subprocess.run(['certutil', '-v', '-dump', file_path], capture_output=True, text=True, check=True)
        certificate_info = result.stdout
        text_output.config(state=tk.NORMAL)
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, certificate_info)
        text_output.config(state=tk.DISABLED)
    except subprocess.CalledProcessError:
        text_output.config(state=tk.NORMAL)
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, "Error: Certificate information not found.")
        text_output.config(state=tk.DISABLED)

# Initialize the main window
root = tk.Tk()
root.title("Certificate Viewer")
root.geometry("800x600")  # Set initial size
root.resizable(True, True)  # Allow resizing

# Set window icon
root.iconbitmap("icone.ico")  # Replace "icone.ico" with the path to your icon file

style = ttk.Style(root)
style.theme_use('clam')  # Use a theme for consistent appearance, 'clam' is just an example

# Customizing button appearance
select_button = ttk.Button(root, text="Select .exe File", command=select_file)
select_button.pack(pady=20, padx=20)

# Customizing the text widget with scrollbar
text_output = scrolledtext.ScrolledText(root, height=20, width=80, wrap=tk.WORD)
text_output.pack(padx=10, pady=10, expand=True, fill='both')
text_output.config(state=tk.DISABLED)

# Run the Tkinter event loop
root.mainloop()
