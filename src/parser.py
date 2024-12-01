import tkinter as tk
from tkinter import simpledialog

class Parser:
    def __init__(self, lexemes):
        """
        Initialize the syntax analyzer with the lexemes.
        lexemes: List of tuples, where each tuple contains a lexeme and its classification.
        """
        self.lexemes = lexemes
        self.cursor = 0
        self.errors = []
        self.symbol_table = {}
        self.IT = None  # Special key to hold the most recent VISIBLE output

    def current_token(self):
        """Return the current token as a tuple or None if out of bounds."""
        return self.lexemes[self.cursor] if self.cursor < len(self.lexemes) else None

    def consume(self, expected_type=None):
        """
        Consume the current token if it matches the expected type.
        Raise a syntax error if the token does not match.
        """
        if self.current_token() is None:
            raise SyntaxError("Unexpected end of input.")
        if expected_type is None or self.current_token()[1] == expected_type:
            print(f"Consuming token: {self.current_token()[0]} with Classification: {self.current_token()[1]}")
            self.cursor += 1
            return self.current_token()
        raise SyntaxError(f"Expected {expected_type} got {self.current_token()[1]} at token '{self.current_token()[0]}'.")

    def check_for_valid_inline_comments(self):
        if self.current_token()[1] == "Single Line Comment":
            if self.lexemes[self.cursor + 1][1] == "Linebreak":
                self.consume("Single Line Comment")

    def parse_program(self):
        """Parse the entire program."""
        try:
            # Handle comments outside Starting Program
            while self.current_token():
                if self.current_token()[1] == "Starting Program":
                    break
                if self.current_token()[1] == "Linebreak":
                    self.consume("Linebreak")
                elif self.current_token()[1] == "Single Line Comment":
                    self.consume("Single Line Comment")
                elif self.current_token()[1] == "Starting Multiple Line Comment":
                    self.consume("Starting Multiple Line Comment")
                    while self.current_token() and self.current_token()[1] != "Ending Multiple Line Comment":
                        self.consume()
                    self.consume("Ending Multiple Line Comment")
                else:
                    self.errors.append(f"Unexpected token '{self.current_token()[0]}'.")

            self.consume("Starting Program")  # HAI
            self.check_for_valid_inline_comments()
            self.consume("Linebreak")

            while self.current_token() and self.current_token()[1] != "Ending Program":
                self.parse_statement()

            self.consume("Ending Program")  # KTHXBYE

            print("Program is syntactically correct.")
            print("Final Symbol Table:")
            for var, attributes in self.symbol_table.items():
                print(f"{var}: {attributes}")

            print(f"Value of IT: {self.IT}")

        except SyntaxError as e:
            print(f"Syntax Error: {e}")

    def parse_statement(self):
        """Handle a single statement."""
        token_type = self.current_token()[1]

        if token_type == "Linebreak":
            self.consume("Linebreak")

        elif token_type == "Variable Declaration":
            self.parse_variable_declaration()

        elif token_type == "Variable Identifier":
            self.parse_assignment()

        elif token_type == "Output Keyword":
            self.parse_visible()

        elif token_type == "Input Keyword":
            self.parse_input()

        elif token_type == "Typecasting":
            self.parse_typecasting()

        elif token_type in ["Arithmetic Operation", "Boolean Operation", "Comparison Operation", "SMOOSH"]:
            self.IT = self.parse_expression()

        elif token_type == "Conditional Statement":
            self.parse_conditional()

        elif token_type == "Loop Start":
            self.parse_loop()

        elif token_type == "Function Start":
            self.parse_function()

        elif token_type == "Function Call":
            self.parse_function_call()

        elif token_type == "Single Line Comment":
            self.consume("Single Line Comment")

        elif token_type == "Starting Multiple Line Comment":
            self.consume("Starting Multiple Line Comment")
            while self.current_token() and self.current_token()[1] != "Ending Multiple Line Comment":
                self.consume()
            self.consume("Ending Multiple Line Comment")

        else:
            self.consume()

    def parse_variable_declaration(self):
        """Parse a variable declaration."""
        self.consume("Variable Declaration")  # I HAS A
        variable_name = self.current_token()[0]
        self.symbol_table[variable_name] = {"type": "NOOB", "value": None}
        self.consume("Variable Identifier")

        if self.current_token() and self.current_token()[1] == "Variable Assignment":  # ITZ
            self.consume("Variable Assignment")
            if self.current_token()[1] == "String Delimiter":
                self.consume("String Delimiter")
                value = self.current_token()[0]
                self.consume("Literal")
                self.consume("String Delimiter")
                value_type = "YARN"
            else:
                value = self.parse_expression()
                value_type = self.determine_type(value)
            self.symbol_table[variable_name].update({"type": value_type, "value": value})

    def parse_assignment(self):
        """Parse a variable assignment."""
        variable_name = self.current_token()[0]
        if variable_name not in self.symbol_table:
            raise SyntaxError(f"Variable '{variable_name}' not declared.")
        self.consume("Variable Identifier")
        if self.current_token()[1] == "Variable Assignment":  # R
            print("tite")
            self.consume("Variable Assignment")
            if self.current_token()[0] == "MAEK":
                self.consume("Typecasting")  # MAEK
                self.consume("Typecasting")  # A
                value = self.parse_expression()
                # our coding way should change, we must only get the type AFTER checking the syntax
                new_type = self.current_token()[0]
                self.consume("Type Identifier")
                self.IT = self.cast_value(value, new_type)
                print(self.IT)
                # if we are going to typecast, or change its value, we get its type, and change the value using cast_value to associate what it should be in
                self.symbol_table[variable_name].update({"type": new_type, "value": self.cast_value(value, new_type)})
                print(self.symbol_table)
            else:
                if self.current_token()[1] == "String Delimiter":
                    self.consume("String Delimiter")
                    value = self.current_token()[0]
                    self.consume("Literal")
                    self.consume("String Delimiter")
                    value_type = "YARN"
                else:
                    value = self.parse_expression()
                    value_type = self.determine_type(value)
                self.symbol_table[variable_name].update({"type": value_type, "value": value})
        elif self.current_token()[1] == "Typecasting":  # IS NOW A
            self.consume("Typecasting")  # IS NOW A
            new_type = self.current_token()[0]
            if new_type not in ["NUMBR", "NUMBAR", "YARN", "TROOF"]:
                raise SyntaxError(f"Invalid type identifier: {new_type}")
            self.consume("Type Identifier")
            self.symbol_table[variable_name]["type"] = new_type
            self.symbol_table[variable_name]["value"] = self.cast_value(self.symbol_table[variable_name]["value"], new_type)

    def parse_visible(self):
        """Parse and execute a VISIBLE statement."""
        self.consume("Output Keyword")  # VISIBLE
        output = []
        while self.current_token() and self.current_token()[1] != "Linebreak":
            if self.current_token()[1] == "Operator" and self.current_token()[0] == "+":
                self.consume("Operator")
            elif self.current_token()[1] == "Operator Separator":
                self.consume("Operator Separator")
            elif self.current_token()[1] == "String Delimiter":
                self.consume("String Delimiter")
                output.append(self.current_token()[0])
                self.consume("Literal")
                self.consume("String Delimiter")
            elif self.current_token()[1] == "Literal":
                output.append(self.current_token()[0])
                self.consume("Literal")
            elif self.current_token()[1] == "Variable Identifier":
                output.append(self.symbol_table[self.current_token()[0]]["value"])
                self.consume("Variable Identifier")
            elif self.current_token()[1] == "Arithmetic Operation":
                output.append(self.parse_expression())
            elif self.current_token()[1] == "Boolean Operation":
                output.append(self.parse_expression())
            elif self.current_token()[1] == "Comparison Operation":
                output.append(self.parse_expression())
            else:
                self.consume()
        self.IT = ''.join(map(str, output))
        print(f"VISIBLE: {self.IT}")
        self.consume("Linebreak")

    def parse_input(self):
        """Parse and execute a GIMMEH statement with a popup for input."""
        self.consume("Input Keyword")  # GIMMEH
        variable_name = self.current_token()[0]
        if variable_name not in self.symbol_table:
            raise SyntaxError(f"Variable '{variable_name}' not declared.")
        self.consume("Variable Identifier")

        # Create a popup to get the input value
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        input_value = simpledialog.askstring("Input", f"GIMMEH {variable_name}:")
        root.destroy()

        # Debug print statements
        print(f"Input value received: {input_value}")
        print(f"Updating variable '{variable_name}' in symbol table.")

        # Store the input value as a string
        self.symbol_table[variable_name]["value"] = input_value
        self.symbol_table[variable_name]["type"] = "YARN"  # Default type is YARN (string)

        # Debug print statements
        print(f"Updated symbol table: {self.symbol_table}")

        self.check_for_valid_inline_comments()
        self.consume("Linebreak")

    def parse_typecasting(self):
        """Handle typecasting using MAEK or IS NOW A."""
        self.consume("Typecasting")  # MAEK
        variable_name = self.current_token()[0]
        if variable_name not in self.symbol_table:
            raise SyntaxError(f"Variable '{variable_name}' not declared.")
        self.consume("Variable Identifier")
        new_type = self.current_token()[0]
        self.consume("Type Identifier")  # e.g., NUMBR, YARN
        self.symbol_table[variable_name]["type"] = new_type
        self.symbol_table[variable_name]["value"] = self.cast_value(self.symbol_table[variable_name]["value"], new_type)

    def parse_conditional(self):
        """Parse an if-else conditional (O RLY?)."""
        self.consume("Conditional Statement")  # O RLY?
        self.consume("Linebreak")
        condition = self.IT

        if self.current_token()[0] == "YA RLY":
            self.consume("Conditional Statement")
            self.consume("Linebreak")
            if condition:
                while self.current_token() and self.current_token()[0] not in ["NO WAI", "OIC"]:
                    self.parse_statement()
            else:
                while self.current_token() and self.current_token()[0] != "NO WAI":
                    self.consume()
        if self.current_token()[0] == "NO WAI":
            self.consume("Conditional Statement")
            self.consume("Linebreak")
            if not condition:
                while self.current_token() and self.current_token()[0] != "OIC":
                    self.parse_statement()
        self.consume("Conditional Statement")  # OIC

    def parse_loop(self):
        """Parse a loop construct (IM IN YR)."""
        self.consume("Loop Start")  # IM IN YR
        label = self.current_token()[0]
        self.consume("Variable Identifier")
        operation = self.current_token()[0]  # UPPIN or NERFIN
        self.consume("Loop Operation")
        self.consume("Construct")  # YR
        variable = self.current_token()[0]
        self.consume("Variable Identifier")
        condition = None

        if self.current_token()[1] == "Loop Statement":  # TIL or WILE
            condition_type = self.current_token()[0]
            self.consume("Loop Statement")
            condition = self.parse_expression()

        while self.evaluate_loop_condition(variable, operation, condition, condition_type):
            while self.current_token() and self.current_token()[1] != "Loop End":
                self.parse_statement()
            self.symbol_table[variable]["value"] += 1 if operation == "UPPIN" else -1

        self.consume("Loop End")  # IM OUTTA YR
        self.consume("Variable Identifier")  # Label

    def parse_function(self):
        """Parse a function definition (HOW IZ I)."""
        self.consume("Function Start")  # HOW IZ I
        function_name = self.current_token()[0]
        self.consume("Variable Identifier")
        parameters = []
        if self.current_token()[1] == "Construct":
            self.consume("Construct")
            parameters.append(self.current_token()[0])
            self.consume("Variable Identifier")
            while self.current_token()[1] == "Operator Separator":
                self.consume("Operator Separator")
                self.consume("Construct")
                parameters.append(self.current_token()[0])
                self.consume("Variable Identifier")
        self.consume("Linebreak")
        while self.current_token() and self.current_token()[1] != "Function End":
            self.parse_statement()
        self.consume("Function End")  # IF U SAY SO

    def parse_function_call(self):
        """Parse a function call (I IZ)."""
        self.consume("Function Call")  # I IZ
        function_name = self.current_token()[0]
        self.consume("Function Identifier")
        arguments = []
        if self.current_token()[1] == "Construct":
            self.consume("Construct")
            arguments.append(self.parse_expression())
            while self.current_token()[1] == "Operator Separator":
                self.consume("Operator Separator")
                self.consume("Construct")
                arguments.append(self.parse_expression())
        if self.current_token()[1] == "Arity Delimiter":
            self.consume("Arity Delimiter")  # MKAY
        self.consume("Linebreak")

    def parse_expression(self):
        """Parse and evaluate an expression."""
        if self.current_token()[1] == "Arithmetic Operation":
            return self.parse_arithmetic()
        elif self.current_token()[1] == "Boolean Operation":
            return self.parse_boolean()
        elif self.current_token()[1] == "Comparison Operation":
            return self.parse_comparison()
        elif self.current_token()[1] == "String Concatenation":
            return self.parse_smoosh()
        elif self.current_token()[1] in ["Literal", "String Delimiter", "Variable Identifier"]:
            return self.parse_literal_or_variable()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token()[0]}")

    def parse_arithmetic(self):
        """Handle complex arithmetic operations, including nested expressions."""
        operator = self.current_token()[0]
        self.consume("Arithmetic Operation")
        left = self.parse_expression()  # Left operand
        self.consume("Operator Separator")  # AN
        right = self.parse_expression()  # Right operand
        return self.perform_arithmetic(left, right, operator)

    def parse_boolean(self):
        """Parse boolean operations."""
        operator = self.current_token()[0]
        self.consume("Boolean Operation")
        if operator == "NOT":
            value = self.parse_expression()
            print("debug: ",value)
            if self.cast_value(value,"TROOF") == "WIN":
                return "FAIL"
            elif self.cast_value(value,"TROOF") == "FAIL":
                return "WIN"
        left = self.parse_expression()  # Left operand
        self.consume("Operator Separator")  # AN
        right = self.parse_expression()  # Right operand
        if operator == "BOTH OF":
            print("debug: ",left,right)
            if self.cast_value(left,"TROOF") == "WIN" and self.cast_value(right,"TROOF") == "WIN":
                return "WIN"
            return "FAIL"
        elif operator == "EITHER OF":
            if (self.cast_value(left,"TROOF") == "WIN") or (self.cast_value(right,"TROOF") == "WIN"):
                return "WIN"
            return "FAIL"
        elif operator == "WON OF":
            if self.cast_value(left,"TROOF") == "WIN" and self.cast_value(right,"TROOF") == "FAIL":
                return "WIN"
            elif self.cast_value(left,"TROOF") == "FAIL" and self.cast_value(right,"TROOF") == "WIN":
                return "WIN"
            return "FAIL"
        elif operator == "ALL OF":
            values = [left]
            while self.current_token() and self.current_token()[1] != "Arity Delimiter":
                self.consume("Operator Separator")
                values.append(self.parse_expression())
            self.consume("Arity Delimiter")  # MKAY
            if "FAIL" in values:
                return "FAIL"
            return "WIN"
        elif operator == "ANY OF":
            values = [left]
            while self.current_token() and self.current_token()[1] != "Arity Delimiter":
                self.consume("Operator Separator")
                values.append(self.parse_expression())
            self.consume("Arity Delimiter")  # MKAY
            if "WIN" in values:
                return "WIN"
            return "FAIL"
        else:
            raise SyntaxError(f"Unexpected boolean operator: {operator}")

    def parse_literal_or_variable(self):
        """Parse a literal or variable."""
        if self.current_token()[1] == "String Delimiter":
            return self.parse_literal()
        elif self.current_token()[1] == "Literal":
            return self.parse_literal()
        elif self.current_token()[1] == "Variable Identifier":
            return self.parse_variable()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token()[0]}")

    def parse_literal(self):
        """Parse a literal which can be either a string or a number."""
        if self.current_token()[1] == "String Delimiter":
            self.consume("String Delimiter")
            literal_value = self.current_token()[0]
            self.consume("Literal")
            self.consume("String Delimiter")
            return literal_value
        elif self.current_token()[1] == "Literal":
            literal_value = self.current_token()[0]
            self.consume("Literal")
            # Convert the literal to its appropriate type
            if literal_value.isdigit():
                return int(literal_value)
            try:
                return float(literal_value)
            except ValueError:
                return literal_value
        else:
            self.errors.append(f"Unexpected literal at token '{self.current_token()[0]}'.")
            raise SyntaxError(f"Unexpected literal at token '{self.current_token()[0]}'.")

    def perform_arithmetic(self, left, right, operator):
        """Perform arithmetic based on the operator."""
        left = self.cast_to_number(left)
        right = self.cast_to_number(right)
        # Ensure that left and right are numbers
        if isinstance(left, str):
            try:
                left = float(left) if '.' in left else int(left)
            except ValueError:
                raise TypeError(f"Invalid operand type for arithmetic: {left}")
        if isinstance(right, str):
            try:
                right = float(right) if '.' in right else int(right)
            except ValueError:
                raise TypeError(f"Invalid operand type for arithmetic: {right}")

        if operator == "SUM OF":
            return left + right
        elif operator == "DIFF OF":
            return left - right
        elif operator == "PRODUKT OF":
            return left * right
        elif operator == "QUOSHUNT OF":
            return left / right
        elif operator == "MOD OF":
            return left % right
        elif operator == "BIGGR OF":
            return max(left, right)
        elif operator == "SMALLR OF":
            return min(left, right)
        else:
            raise ValueError(f"Unknown operator: {operator}")



    def parse_comparison(self):
        """Parse comparison operations and set a flag if the right side is nested."""
        operator = self.current_token()[0]
        self.consume("Comparison Operation")
        left = self.parse_expression()
        self.consume("Operator Separator")  # AN
        next_token = self.current_token()
        is_right_nested = next_token[1] in {"Arithmetic Operation", "Comparison Operation", "Boolean Operation"}
        right = self.parse_expression()
        if is_right_nested:
            if operator == "BOTH SAEM":
                return "WIN" if left == right else "FAIL"
            elif operator == "DIFFRINT":
                return "WIN" if left != right else "FAIL"
            print("Debug: Right side is nested.")
        else:
            print("Debug: Right side is not nested.")
            print("debug: ", left, right)
            if operator == "BOTH SAEM":
                return "WIN" if left == right else "FAIL"
            elif operator == "DIFFRINT":
                return "WIN" if left != right else "FAIL"
        raise SyntaxError(f"Unexpected comparison operator: {operator}")

    def parse_variable(self):
        """Parse and return the value of a variable."""
        var_name = self.current_token()[0]
        if var_name not in self.symbol_table:
            raise SyntaxError(f"Variable '{var_name}' not declared.")
        self.consume("Variable Identifier")
        return self.symbol_table[var_name]["value"]

    def determine_type(self, value):
        """Determine the LOLCode type of a value."""
        if isinstance(value, int):
            return "NUMBR"
        elif isinstance(value, float):
            return "NUMBAR"
        elif isinstance(value, bool):
            return "TROOF"
        elif isinstance(value, str):
            if value in ["WIN", "FAIL"]:
                return "TROOF"
            return "YARN"
        else:
            return "NOOB"

    def cast_value(self, value, target_type):
        """Cast a value to the specified LOLCode type."""
        if target_type == "NUMBR":
            try:
                return int(value)
            except ValueError:
                raise SyntaxError(f"Cannot cast value '{value}' to NUMBR")
        elif target_type == "NUMBAR":
            try:
                return float(value)
            except ValueError:
                raise SyntaxError(f"Cannot cast value '{value}' to NUMBAR")
        elif target_type == "YARN":
            return str(value)
        elif target_type == "TROOF":
            if isinstance(value, str):
                if value == "WIN":
                    return "WIN"
                elif value == "FAIL":
                    return "FAIL"
                elif len(value) > 0:
                    return "WIN"
                else:
                    return "FAIL"
            if value:
                return "WIN"
            else:
                return "FAIL"
        elif target_type == "NOOB":
            return None
        else:
            raise ValueError(f"Invalid type casting to {target_type}")

    def cast_to_number(self, value):
        """Cast a value to a number (int or float)."""
        if value == "FAIL":
            return 0
        if value == "WIN":
            return 1
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                raise TypeError(f"Cannot cast value to number: {value}")

    def evaluate_loop_condition(self, variable, operation, condition, condition_type):
        """Evaluate loop conditions (TIL or WILE)."""
        value = self.symbol_table[variable]["value"]
        if condition_type == "TIL":
            return value != condition
        elif condition_type == "WILE":
            return value == condition
        return True

    def parse_smoosh(self):
        """Parse and execute a SMOOSH statement."""
        self.consume("String Concatenation")  # SMOOSH
        output = []
        while self.current_token() and self.current_token()[1] != "Linebreak":
            if self.current_token()[1] == "Operator Separator":
                self.consume("Operator Separator")
            elif self.current_token()[1] == "String Delimiter":
                self.consume("String Delimiter")
                output.append(self.current_token()[0])
                self.consume("Literal")
                self.consume("String Delimiter")
            elif self.current_token()[1] == "Literal":
                output.append(self.current_token()[0])
                self.consume("Literal")
            elif self.current_token()[1] == "Variable Identifier":
                output.append(self.symbol_table[self.current_token()[0]]["value"])
                self.consume("Variable Identifier")
            else:
                self.consume()
        return ''.join(map(str, output))