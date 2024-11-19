import re
import tkinter as tk
from tkinter import ttk


class Interpreter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LOLCODE Interpreter")

        # synbol table
        self.symtree = ttk.Treeview(self.root, columns=("Lexeme", "Token", "Category"), show="headings")
        self.symtree.heading("Lexeme", text="Lexeme")
        self.symtree.heading("Token", text="Token")
        self.symtree.heading("Category", text="Category")
        self.symtree.pack(fill=tk.BOTH, expand=True)

        # terminal output (if needed)
        self.terminal = tk.Text(self.root, wrap=tk.WORD, height=10)
        self.terminal.pack(fill=tk.BOTH, expand=True)

    def display_symboltable(self, symbol_table):
        # tree view
        for item in self.symtree.get_children():
            self.symtree.delete(item)

        # put lexemes in the tree view
        for item in symbol_table:
            col1_value = item[0]
            col2_value = item[1]
            col3_value = item[2] if len(item) > 2 else ''
            self.symtree.insert('', 'end', values=(col1_value, col2_value, col3_value))

    def display_terminal(self, toprint):
        # terminal output
        self.terminal.delete(1.0, tk.END)
        for item in toprint:
            self.terminal.insert(tk.END, item + '\n')

    def mainloop(self):
        self.root.mainloop()



Interpreter().mainloop()
