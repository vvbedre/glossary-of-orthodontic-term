import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
from tkinter.font import Font

class OrthodonticGlossaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Orthodontic Glossary")
        self.root.geometry("800x500")
        self.root.configure(bg="#f6f8fa")
        self.root.minsize(400, 300)

        # Fonts
        self.title_font = Font(family="Segoe UI", size=22, weight="bold")
        self.term_font = Font(family="Segoe UI", size=16, weight="bold")
        self.definition_font = Font(family="Segoe UI", size=13)
        self.entry_font = Font(family="Segoe UI", size=13)

        # Accent color
        self.accent = "#1976d2"
        self.card_bg = "#ffffff"
        self.shadow = "#e3e7ed"

        # Data
        self.glossary_data = []
        self.load_data()

        # --- HEADER ---
        self.title_label = tk.Label(
            self.root,
            text="Orthodontic Glossary",
            font=self.title_font,
            bg="#f6f8fa",
            fg=self.accent,
            pady=18
        )
        self.title_label.pack(anchor="center")

        # --- SEARCH BAR ---
        self.search_frame = tk.Frame(self.root, bg="#f6f8fa")
        self.search_frame.pack(pady=(0, 10), padx=0, fill=tk.X)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            self.search_frame,
            textvariable=self.search_var,
            font=self.entry_font,
            bg=self.card_bg,
            relief=tk.FLAT,
            highlightthickness=2,
            highlightbackground=self.shadow,
            highlightcolor=self.accent,
            width=1
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=7, padx=(30, 0))
        self.search_entry.insert(0, "Search for a term…")
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.add_placeholder)
        self.search_entry.bind("<KeyRelease>", self.update_autocomplete)
        self.search_entry.bind("<Return>", self.search_term)

        self.search_button = tk.Button(
            self.search_frame,
            text="🔍",
            command=self.search_term,
            bg=self.accent,
            fg="white",
            font=self.entry_font,
            relief=tk.FLAT,
            padx=16,
            pady=2,
            borderwidth=0,
            activebackground="#1565c0"
        )
        self.search_button.pack(side=tk.LEFT, padx=(6, 30), ipady=2)

        # --- AUTOCOMPLETE ---
        self.autocomplete_listbox = tk.Listbox(
            self.root,
            height=5,
            font=self.entry_font,
            bg=self.card_bg,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=self.shadow,
            selectbackground=self.accent,
            selectforeground="white"
        )
        self.autocomplete_listbox.bind("<Double-Button-1>", self.select_autocomplete)

        # --- RESULT CARD ---
        self.card_frame = tk.Frame(self.root, bg=self.shadow)
        self.card_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))

        self.result_card = tk.Frame(self.card_frame, bg=self.card_bg, bd=0, relief=tk.FLAT)
        self.result_card.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.term_display = tk.Label(
            self.result_card,
            text="",
            font=self.term_font,
            bg=self.card_bg,
            fg=self.accent,
            anchor="w",
            wraplength=1,
            pady=10
        )
        self.term_display.pack(anchor="w", fill=tk.X, padx=18, pady=(10, 0), expand=False)  # Only fill X, do not expand vertically

        self.definition_display = tk.Label(
            self.result_card,
            text="",
            font=self.definition_font,
            bg=self.card_bg,
            fg="#222",
            anchor="nw",
            wraplength=1,
            justify=tk.LEFT,
            pady=10
        )
        self.definition_display.pack(anchor="w", fill=tk.BOTH, expand=True, padx=18, pady=(0, 18))  # Fill and expand vertically

        self.update_autocomplete_list()
        self.root.bind('<Configure>', self.on_resize)

    def clear_placeholder(self, event=None):
        if self.search_entry.get() == "Search for a term…":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="#222")

    def add_placeholder(self, event=None):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search for a term…")
            self.search_entry.config(fg="#888")

    def on_resize(self, event=None):
        width = self.result_card.winfo_width()
        if width < 100:
            width = 100
        self.term_display.config(wraplength=width-40)
        self.definition_display.config(wraplength=width-40)

    def load_data(self):
        if os.path.exists("orthodontic_glossary.csv"):
            try:
                df = pd.read_csv("orthodontic_glossary.csv")
                self.glossary_data = df.to_dict('records')
            except:
                self.glossary_data = []
        else:
            self.glossary_data = []
        if not self.glossary_data:
            self.glossary_data = [
                {"term": "Malocclusion", "definition": "Misalignment of teeth or incorrect relation between the teeth of the two dental arches."},
                {"term": "Bracket", "definition": "A small attachment bonded to teeth to hold archwires in place."},
                {"term": "Archwire", "definition": "A wire engaged in orthodontic attachments that can be used to cause tooth movement."}
            ]

    def search_term(self, event=None):
        search_text = self.search_var.get().strip().lower()
        if not search_text or search_text == "search for a term…":
            messagebox.showinfo("Info", "Please enter a search term")
            return
        found_terms = [term for term in self.glossary_data if search_text in term["term"].lower()]
        if found_terms:
            self.display_term(found_terms[0])
            self.autocomplete_listbox.pack_forget()
        else:
            messagebox.showinfo("Not Found", f"No term found matching '{search_text}'")
            self.clear_display()

    def display_term(self, term_data):
        self.term_display.config(text=term_data["term"])
        self.definition_display.config(text=term_data.get("definition", ""))

    def clear_display(self):
        self.term_display.config(text="")
        self.definition_display.config(text="")

    def update_autocomplete_list(self):
        self.terms_list = [term["term"] for term in self.glossary_data]

    def update_autocomplete(self, event=None):
        search_text = self.search_var.get().strip().lower()
        self.autocomplete_listbox.delete(0, tk.END)
        if not search_text or search_text == "search for a term…":
            self.autocomplete_listbox.pack_forget()
            return
        matches = 0
        for term in self.terms_list:
            if search_text in term.lower():
                self.autocomplete_listbox.insert(tk.END, term)
                matches += 1
                if matches >= 5:
                    break
        if matches > 0:
            self.autocomplete_listbox.pack(fill=tk.X, padx=60, pady=(0, 0))
        else:
            self.autocomplete_listbox.pack_forget()

    def select_autocomplete(self, event=None):
        if self.autocomplete_listbox.curselection():
            selected_term = self.autocomplete_listbox.get(self.autocomplete_listbox.curselection())
            self.search_var.set(selected_term)
            self.autocomplete_listbox.pack_forget()
            self.search_term()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrthodonticGlossaryApp(root)
    root.mainloop()