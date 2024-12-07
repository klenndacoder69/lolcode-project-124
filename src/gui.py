import tkinter as tk
from tkinter import Scrollbar, filedialog, messagebox, ttk
import os
from lexemes import get_lexemes
from parser import Parser

class InterpreterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LOLCode Interpreter")

        # COLORS
        self.root_bg_color = "#000000"
        self.field_bg_color = "#E4E0E1"
        self.highlight_color = "#000000"
        self.root.configure(bg=self.root_bg_color)

        # APP CAN'T BE RESIZED
        self.root.resizable(width=False, height=False)

        # INITIAL
        self.init_file = tk.StringVar()
        self.init_file.set("     (none)")
        self.lines = []

        # APP DIMENSIONS
        app_width = 1120
        app_height = 626

        # SCREEN DIMENSIONS
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # X, Y  COORDINATES FOR PLACING THE WINDOW IN THE SCREEN
        x = (screen_width/2) - (app_width/2)
        y = (screen_height/2) - (app_height/2)
        
        # CENTER WINDOW IN RUN AND SET APP DIMENSIONS AS THE MINIMUM SIZE   
        self.root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)-30}')
        self.root.minsize(app_width, app_height)

        # CREATE WIDGETS
        self.create_widgets()
    
    def create_widgets(self):
        # MAIN FRAME      
        self.main_frame = tk.Frame(self.root, bg=self.root_bg_color)
        self.main_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

            # GRID CONFIGURATION
        self.main_frame.grid_rowconfigure(0, weight=0, minsize=30)
        self.main_frame.grid_rowconfigure(1, weight=0, minsize=296)
        self.main_frame.grid_rowconfigure(2, weight=0, minsize=40)
        self.main_frame.grid_rowconfigure(3, weight=0, minsize=245)
        
        self.main_frame.grid_columnconfigure(0, weight=0, minsize=390)
        self.main_frame.grid_columnconfigure(1, weight=0, minsize=360)
        self.main_frame.grid_columnconfigure(2, weight=0, minsize=358)

        # ROW 1 : FILE EXPLORER
        self.row1 = tk.Frame(self.main_frame)
        self.row1.grid(row=0, column=0, padx=3, pady=3, sticky="nsew")
            # FILE NAME
        self.file_name = tk.Entry(self.row1, font=('Helvetica', 10), borderwidth=1, relief="solid", state="disabled", textvariable=self.init_file)
        self.file_name.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

            # FILE BUTTON
        self.import_button = tk.Button(self.row1, text="File", font=('Helvetica', 10), borderwidth=1, relief="solid", bg=self.highlight_color, fg="white", command=self.import_file)
        self.import_button.grid(row=0, column=1, sticky="ew")

            # EXPAND FILE NAME
        self.row1.grid_columnconfigure(0, weight=1)

        # ROW 2 COL 1 : TEXT EDITOR
        self.column1 = tk.Frame(self.main_frame)
        self.column1.grid(row=1, column=0, padx=3, pady=3, sticky="nsew")

            # SCROLLBAR SET-UP
        self.editor_scroll = Scrollbar(self.column1)
        self.editor_scroll.grid(row=0, column=1, sticky='ns')

            # TEXT FIELD: TEXT EDITOR
        self.text_editor = tk.Text(self.column1, font=('Helvetica', 10), height=18, width=52, bg=self.field_bg_color, yscrollcommand=self.editor_scroll.set)
        self.text_editor.grid(row=0, column=0)

            # ATTACH SCROLLBAR TO TEXT EDITOR
        self.editor_scroll.config(command=self.text_editor.yview)

        # ROW 2 COL 2 : LIST OF TOKENS
        self.column2 = tk.Frame(self.main_frame)
        self.column2.grid(row=1, column=1, padx=3, pady=3, sticky="nsew")

            # GRID CONFIGURATION
        self.column2.grid_rowconfigure(0, weight=0, minsize=20)
        self.column2.grid_rowconfigure(1, weight=0, minsize=270)

            # LABEL: LEXEMES
        self.col2row1 = tk.Frame(self.column2)
        self.col2row1.grid(row=0, column=0, sticky="nsew")
        self.lexemes_label = tk.Label(self.col2row1, text="LEXEMES", font=('Helvetica', 11, 'bold'), bg=self.root_bg_color, fg="white")
        self.lexemes_label.grid(row=0, column=0, sticky="ew")

            # CENTER LABEL
        self.col2row1.grid_rowconfigure(0, weight=1)
        self.col2row1.grid_columnconfigure(0, weight=1)

            # TABLE : LIST OF TOKENS
        self.col2row2 = tk.Frame(self.column2)
        self.col2row2.grid(row=1, column=0, padx=3, pady=3, sticky="nsew")

            # TREEVIEW STYLING
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview.Heading", background=self.highlight_color, foreground="white", font=('Helvetica', 10))
        style.map("Treeview.Heading", background=[('active', self.highlight_color)])

        style.configure("Treeview", background=self.field_bg_color, font=('Helvetica', 10), fieldbackground=self.field_bg_color)
        style.map("Treeview", background=[('selected', self.root_bg_color)])

            # SET-UP TREEVIEW
        self.list_tokens_table = ttk.Treeview(self.col2row2, columns=("Lexeme", "Classification"), show="headings", height=12)
        self.list_tokens_table.heading("Lexeme", text="Lexeme")
        self.list_tokens_table.heading("Classification", text="Classification")
        self.list_tokens_table.column("Lexeme", width=150)
        self.list_tokens_table.column("Classification", width=179)

            # SCROLL BAR SETUP
        lexeme_scroll = tk.Scrollbar(self.col2row2, orient="vertical", command=self.list_tokens_table.yview)
        lexeme_scroll.grid(row=0, column=1, sticky='ns')  # Use grid for both Treeview and Scrollbar

            # ATTACH SCROLLBAR TO TREEVIEW
        self.list_tokens_table.config(yscrollcommand=lexeme_scroll.set)

            # SET-UP TREEVIEW (2)
        self.list_tokens_table.grid(row=0, column=0, sticky="nsew")
        self.list_tokens_table.tag_configure("custom_font", font=("Helvetica", 12))
        self.list_tokens_table.grid(row=0, column=0, sticky="nsew")

        # ROW 2 COL 3 : SYMBOL TABLE
        self.column3 = tk.Frame(self.main_frame)
        self.column3.grid(row=1, column=2, padx=3, pady=3, sticky="nsew")

            # GRID CONFIGURATION
        self.column3.grid_rowconfigure(0, weight=0, minsize=20)
        self.column3.grid_rowconfigure(1, weight=0, minsize=270)

            # LABEL: SYMBOL TABLE
        self.col3row1 = tk.Frame(self.column3)
        self.col3row1.grid(row=0, column=0, sticky="nsew")
        self.symbol_label = tk.Label(self.col3row1, text="SYMBOL TABLE", font=('Helvetica', 11, 'bold'), fg="white", bg=self.root_bg_color)
        self.symbol_label.grid(row=0, column=0, sticky="ew")

            # CENTER LABEL
        self.col3row1.grid_rowconfigure(0, weight=1)
        self.col3row1.grid_columnconfigure(0, weight=1)

            # TABLE : SYMBOL TABLE
        self.col3row2 = tk.Frame(self.column3)
        self.col3row2.grid(row=1, column=0, padx=3, pady=3, sticky="nsew")

            # SET-UP TREEVIEW
        self.symbol_table = ttk.Treeview(self.col3row2, columns=("Identifier", "Value"), show="headings", height=12)
        self.symbol_table.heading("Identifier", text="Identifier")
        self.symbol_table.heading("Value", text="Value")
        self.symbol_table.column("Identifier", width=149)
        self.symbol_table.column("Value", width=195)

            # SET-UP TREEVIEW (2)
        self.symbol_table.grid(row=0, column=0, sticky="nsew")
        self.symbol_table.tag_configure("custom_font", font=("Helvetica", 12))
        self.symbol_table.grid(row=0, column=0, sticky="nsew")

        # ROW 3 : EXECUTE/RUN BUTTON
        self.row3 = tk.Frame(self.main_frame, bg="white")
        self.row3.grid(row=2, column=0, columnspan=3, padx=3, pady=3, sticky="nsew")

            # EXECUTE BUTTON
        self.execute_button = tk.Button(self.row3, text="EXECUTE", font=('Helvetica', 10, 'bold'), borderwidth=1, bg=self.highlight_color, fg="white", relief="solid", command=self.execute)
        self.execute_button.grid(row=0, column=0, sticky="nsew")

            # EXPAND BUTTON
        self.row3.grid_rowconfigure(0, weight=1)
        self.row3.grid_columnconfigure(0, weight=1)

        # ROW 4 : CONSOLE
        self.row4 = tk.Frame(self.main_frame, bg="white")
        self.row4.grid(row=3, column=0, columnspan=3, padx=3, pady=3, sticky="nsew")

            # TEXT FIELD: CONSOLE
        self.console = tk.Text(self.row4, font=('Helvetica', 10), height=15, width=100, bg=self.field_bg_color, state=tk.DISABLED)
        self.console.grid(row=0, column=0, sticky="nsew")

            # SCROLLBAR SET-UP
        self.console_scroll = Scrollbar(self.row4, command=self.console.yview)
        self.console_scroll.grid(row=0, column=1, sticky='ns')

            # ATTACH SCROLLBAR TO CONSOLE
        self.console.config(yscrollcommand=self.console_scroll.set)

        self.row4.grid_rowconfigure(0, weight=1)
        self.row4.grid_columnconfigure(0, weight=1)
        self.row4.grid_columnconfigure(1, weight=0)

    def import_file(self):
        # OPEN FILE DIALOG
        file_path = filedialog.askopenfilename(title="Select Input File", filetypes=[("Text files", "*.lol")])

        # CHECK IF USER CHOSE A FILE
        if not file_path: 
            messagebox.showwarning("No Directory Selected", "No directory was selected. Please choose a valid directory.")
            return

        # SET FILE NAME 
        self.init_file.set(f'     {os.path.basename(file_path)}')

        # DELETE PREVIOUS TEXT
        self.text_editor.delete(1.0, tk.END)

        # OPEN AND READ FILE
        text_file = open(file_path, 'r')
        input = text_file.read()
        self.text_editor.insert('1.0', input)

    def execute(self):
         # CLEAR THE CONSOLE
        self.console.config(state=tk.NORMAL)
        self.console.delete(1.0, tk.END)
        self.console.config(state=tk.DISABLED)

        # CLEAR THE SYMBOL TABLE
        for row in self.symbol_table.get_children():
            self.symbol_table.delete(row)

        # CLEAR THE LEXEMES TABLE
        for row in self.list_tokens_table.get_children():
            self.list_tokens_table.delete(row)

        # RESET LINES
        self.lines = []

        # GET INPUT FROM THE TEXT EDITOR
        final_input = self.text_editor.get("1.0",tk.END).split("\n")
        
        # REMOVE WHITESPACES
        for line in final_input:
            self.lines.append(line.strip())
        
        # REMOVE EMPTY STRINGS
        self.lines = list(filter(None, self.lines))

        # GET LEXEMES AND FILL TABLE
        lexemes = get_lexemes(self.lines)
        self.fill_table(lexemes)

        # PARSE LEXEMES
        parser = Parser(lexemes, self.update_console, self.display_error)
        symbol_table = parser.parse_program()
        
        if symbol_table == None:
            print("Errors found in the program. Please check the console for more details.")
            return
        # Fill the table with the symbol table data
        self.fill_symbol_table(symbol_table)

    def fill_table(self, lexemes):
        # CLEAR TABLE
        for row in self.list_tokens_table.get_children():
            self.list_tokens_table.delete(row)
        
        # ASSIGN NEW DATA
        for item in lexemes:
            if item[1] == "Linebreak":
                continue
            self.list_tokens_table.insert("", "end", values=(item[0], item[1]))
    
    def fill_symbol_table(self,symbol_table):
        # CLEAR TABLE
        for row in self.symbol_table.get_children():
            self.symbol_table.delete(row)
        
        # ASSIGN NEW DATA
        for item in symbol_table:
            self.symbol_table.insert("", "end", values=(item[0],item[1]))
    
    def update_console(self, message):
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, message + "\n")
        self.console.config(state=tk.DISABLED)
        self.console.see(tk.END)
    
    def display_error(self, message):
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, message + "\n")
        self.console.config(state=tk.DISABLED)
        self.console.see(tk.END)

# CREATE AND RUN THE APP
root = tk.Tk()
app = InterpreterApp(root)
root.mainloop()