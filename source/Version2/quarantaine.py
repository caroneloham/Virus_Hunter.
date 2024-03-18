import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from datetime import datetime
import re
import os


class QuarantineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Antivirus - Mise en Quarantaine")
        self.root.geometry("800x600")
        self.root.configure(bg="#dfe3ee")

        self.style = ttk.Style()
        self.style.configure("Title.TLabel", font=("Helvetica", 18, "bold"), background="#2c3e50", foreground="white",
                             padding=10)
        self.style.configure("Threat.TFrame", background="#ecf0f1", borderwidth=2, relief="groove", padding=10)
        self.style.configure("Threat.TLabel", background="#ecf0f1", font=("Helvetica", 12), padding=5)
        self.style.configure("ThreatDesc.TLabel", background="#ecf0f1", font=("Helvetica", 10), padding=5)
        self.style.configure("Close.TButton", background="#c0392b", foreground="white")

        self.title_label = ttk.Label(self.root, text="Menaces Identifiées", style="Title.TLabel")
        self.title_label.pack(fill=tk.X)

        self.canvas = tk.Canvas(self.root, bg="#dfe3ee")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scroll_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor=tk.NW)

        self.scroll_frame.bind("<Configure>", self.on_frame_configure)

        self.load_quarantine_data()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def load_quarantine_data(self):
        try:
            with open(r"C:\Users\eloha\Desktop\logs\menace_identifiee.txt", "r") as file:
                data = file.read()
                threats = re.findall(r'--- Menace identifiée ---\n(.*?)\n\n', data, re.DOTALL)
                threats.sort(key=self.extract_date)
                self.display_threats(threats)
        except FileNotFoundError:
            self.scroll_area.insert(tk.END, "Fichier introuvable.")

    def extract_date(self, threat):
        match = re.search(r'Date et heure : (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', threat)
        if match:
            return datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
        else:
            return datetime.min

    def delete_threat(self, file_path):
        try:
            os.remove(file_path)
            self.scroll_frame.destroy()
            self.load_quarantine_data()
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier : {e}")

    def display_threats(self, threats):
        for threat in threats:
            threat_frame = ttk.Frame(self.scroll_frame, style="Threat.TFrame")
            threat_frame.pack(fill=tk.X, padx=10, pady=5)

            match_file = re.search(r'Fichier : (.+)', threat)
            match_type = re.search(r'Menace identifiée : (.+)', threat)
            match_date = re.search(r'Date et heure : (.+)', threat)

            if match_file:
                file_label = ttk.Label(threat_frame, text=f"Fichier : {match_file.group(1)}", style="Threat.TLabel")
                file_label.pack(anchor=tk.W, padx=(0, 20), pady=5)
            if match_type:
                type_label = ttk.Label(threat_frame, text=f"Type de menace : {match_type.group(1)}",
                                       style="ThreatDesc.TLabel")
                type_label.pack(anchor=tk.W, padx=(0, 20), pady=2)
            if match_date:
                date_label = ttk.Label(threat_frame, text=f"Date : {match_date.group(1)}", style="ThreatDesc.TLabel")
                date_label.pack(anchor=tk.W, padx=(0, 20), pady=2)

            close_button = ttk.Button(threat_frame, text="✖", style="Close.TButton",
                                      command=lambda f=match_file.group(1): self.delete_threat(f))
            close_button.pack(side=tk.RIGHT)


root = tk.Tk()
app = QuarantineApp(root)
root.mainloop()