import tkinter as tk
from tkinter import ttk, filedialog
import lexemes

class Interpreter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LOLCODE Interpreter")

        # title
        self.title = tk.Label(self.root, text="Detective Cunan1", font=("Arial", 16))
        self.title.pack(pady=10)

        # symbol table
        self.symtree = ttk.Treeview(self.root, columns=("Lexeme", "Classification"), show="headings")
        self.symtree.heading("Lexeme", text="Lexeme")
        self.symtree.heading("Classification", text="Classification")
        self.symtree.pack(fill=tk.BOTH, expand=True)

        # button to select a file
        self.button = tk.Button(self.root, text="Input LOL file", command=self.open_file)
        self.button.pack()

    def display_symboltable(self, dict_lexeme):
        # tree view
        for item in self.symtree.get_children():
            self.symtree.delete(item)

        # put lexemes in the tree view
        for lexeme, classification in dict_lexeme:
            self.symtree.insert('', 'end', values=(lexeme, classification))

    def open_file(self):
        filename = filedialog.askopenfilename(filetypes=[("LOL Files", "*.lol")])
        if filename:
            self.display_symboltable(lexemes.process_file(filename))

    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    Interpreter().mainloop()

