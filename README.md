# LOLCode Interpreter

This project is a LOLCode interpreter implemented using Python and a GUI built with Tkinter. It includes lexeme analysis and syntax parsing for interpreting LOLCode scripts.

## Prerequisites

Ensure you have Python 3.x installed on your system. The following libraries are required:

- `tkinter`
    You can install tkinter by running the following command:
    ```bash
    pip install tk
- Standard Python libraries 

## Project Files

The project consists of the following Python files:

1. `gui.py`: Contains the GUI for the interpreter.
2. `lexemes.py`: Tokenizes and classifies LOLCode syntax.
3. `parser.py`: Syntax parsing and interpretation of LOLCode scripts

## Installation

1. Clone or download this repository.

   ```bash
   git clone https://github.com/klenndacoder69/lolcode-project-124.git

2. Navigate to the project directory:

    ```bash
    cd lolcode-interpreter/source_code

3. Make sure that the following files are present in the directory:

- `gui.py`
- `lexemes.py`
- `parser.py`

## Running the Interpreter

1. Open a terminal or command prompt
2. Navigate to the directory containing project files

    ```bash
    cd lolcode-interpreter/source_code

3. Run the following command

    ```bash
    python gui.py

This will launch the python LOLCode interpreter GUI

## How to Use the Interpreter

1. **Load a File**:
   - Click on the `File` button to select a LOLCode file (`*.lol`).
   - The file content will be loaded into the text editor.

2. **Edit Code**:
   - You can directly edit the LOLCode in the text editor.

3. **Execute Code**:
   - Click on the `EXECUTE` button to run the LOLCode script.

4. **View Output**:
   - The output of the script will appear in the console area.
   - Tokens and their classifications will be displayed in the Lexemes table.
   - The Symbol Table displays the assignment of variables and values. 

