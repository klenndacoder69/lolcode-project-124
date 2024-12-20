import tkinter as tk
from tkinter import simpledialog

class Parser:
    def __init__(self, lexemes,  output_callback=None, error_callback=None):
        """
        Initialize the syntax analyzer with the lexemes.
        lexemes: List of tuples, where each tuple contains a lexeme and its classification.
        """
        self.lexemes = lexemes
        self.cursor = 0
        self.errors = []
        self.symbol_table = {}
        self.IT = None  # Special key to hold the most recent VISIBLE output
        self.output_callback = output_callback
        self.error_callback = error_callback # HERE FOR SAVED POINT
        self.declare_flag = False
        self.list_of_functions = []
        self.function_locations = {}
        self.current_line = 1
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
            if self.current_token()[1] == "Linebreak":
                self.current_line += 1
            self.cursor += 1
            return self.current_token()
        error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Expected {expected_type} got {self.current_token()[1]} at token '{self.current_token()[0]}'." # SAVE POINT
        if self.error_callback:
            self.error_callback(error_message)
        raise SyntaxError(error_message)

    def check_for_valid_inline_comments(self):
        if self.current_token()[1] == "Single Line Comment":
            if self.lexemes[self.cursor + 1][1] == "Linebreak":
                self.consume("Single Line Comment")

    def parse_program(self):
        """Parse the entire program."""
        variables = []
        values = []
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
                    self.parse_multiline_comment()
                elif self.current_token()[1] == "Function Start":
                    self.parse_function()
                else:
                    self.errors.append(f"Unexpected token '{self.current_token()[0]}'.")
                    error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Error while parsing program. Comments are only allowed before the start of the program." # SAVE POINT
                    if self.error_callback:
                        self.error_callback(error_message)
                    raise SyntaxError(error_message)
            self.consume("Starting Program")  # HAI
            self.check_for_valid_inline_comments()
            self.consume("Linebreak")

            while self.current_token() and self.current_token()[1] != "Ending Program":
                if self.errors:
                    print(self.errors)
                    print("Error occurred at line: ", self.current_line)
                    return None
                self.parse_statement()

            self.consume("Ending Program")  # KTHXBYE
            if self.current_token() is not None: # here we address comments made after the end of the program (no other tokens are allowed except for comments)
                while self.current_token() is not None:
                    if self.current_token()[1] == "Linebreak":
                        self.consume("Linebreak")
                    elif self.current_token()[1] == "Single Line Comment":
                        self.consume("Single Line Comment")
                    elif self.current_token()[1] == "Starting Multiple Line Comment":
                        self.parse_multiline_comment()
                    else:
                        self.errors.append(f"Unexpected token '{self.current_token()[0]}'.")
                        error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Error while parsing program. Comments are only allowed at the end of the program" # SAVE POINT
                        if self.error_callback:
                            self.error_callback(error_message)
                        raise SyntaxError(error_message)
            print("Program is syntactically correct.")
            print("Final Symbol Table:")
            for var, attributes in self.symbol_table.items():
                print(f"{var}: {attributes}")
            if 'IT'not in self.symbol_table:
                variables.append('IT')
                values.append(self.IT)
            for var, attributes in self.symbol_table.items():
                value = attributes.get('value')
                variables.append(var)
                values.append(value)
                print(f"{var}: {value}")
            print(variables,values)

        except SyntaxError as e:
            print("check if it goes here")
            print(f"Syntax Error: {e}")
        return list(zip(variables, values))

    def parse_multiline_comment(self):
        ''' Parse a multiline comment. '''
        self.consume("Starting Multiple Line Comment")
        while self.current_token() and self.current_token()[1] != "Ending Multiple Line Comment":
            self.consume()
        self.consume("Ending Multiple Line Comment")
    
    def parse_variable_declaration_block(self):
        ''' Parse a variable declaration block. '''
        if self.declare_flag:
            print("ARE YOU HERE")
            self.errors.append(f"Unexpected self.current_token() '{self.current_token()[0]}'.")
            error_message = f"Error occurred at line {self.current_line}, Unexpected self.current_token() '{self.current_token()[0]}'.\n Syntax Error: Error while parsing declare variables. Only one declare variables block is allowed." # SAVE POINT
            if self.error_callback:
                self.error_callback(error_message)
            raise SyntaxError(error_message)
        self.consume("Starting Declare Variables")
        self.consume("Linebreak")
        while self.current_token() and self.current_token()[1] != "Ending Declare Variables":
            # we limit what we want to consume inside the variable declaration block
            # the possible tokens are:
            # Linebreak, Single Line Comment, Variable Declaration, Multiple Line Comment
            if self.current_token()[1] == "Single Line Comment":
                self.consume("Single Line Comment")
            elif self.current_token()[1] == "Starting Multiple Line Comment":
                self.parse_multiline_comment()
            elif self.current_token()[1] == "Linebreak":
                self.consume("Linebreak")
            elif self.current_token()[1] == "Variable Declaration":
                self.parse_variable_declaration()
            
            else:
                self.errors.append(f"Unexpected self.current_token() '{self.current_token()[0]}'.")
                error_message = f"Error occurred at line {self.current_line}, Unexpected self.current_token() '{self.current_token()[0]}'.\n Syntax Error: Error while parsing declare variables." # SAVE POINT
                if self.error_callback:
                    self.error_callback(error_message)
                raise SyntaxError(error_message) # SAVE POINT
        self.consume("Ending Declare Variables")
        self.consume("Linebreak")
        self.declare_flag = True
        
    def parse_statement(self):
        """Handle a single statement."""
        token_type = self.current_token()[1]

        if token_type == "Linebreak":
            self.consume("Linebreak")
        
        # check for the starting of a variable declaration
        elif token_type == "Starting Declare Variables":
            self.parse_variable_declaration_block()

        elif token_type == "Variable Identifier":
            # we need self.IT for checking conditions later (specifically in WTF?)
            self.IT = self.parse_assignment()

        elif token_type == "Output Keyword":
            self.parse_visible()

        elif token_type == "Input Keyword":
            self.parse_input()

        elif token_type == "Typecasting":
            self.parse_typecasting()

        elif token_type in ["Arithmetic Operation", "Boolean Operation", "Comparison Operation", "SMOOSH"]:
            # we need self.IT for checking conditions later
            self.IT = self.parse_expression()

        elif token_type == "Conditional Statement":
            self.parse_conditional()

        elif token_type == "Case Statement":
            self.parse_case()

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
            self.errors.append(f"Unexpected self.current_token() '{self.current_token()[0]}'.")
            error_message = f"Error occurred at line {self.current_line}, Unexpected self.current_token() '{self.current_token()[0]}'.\n Syntax Error: Error while parsing statement." # SAVE POINT
            if self.error_callback:
                self.error_callback(error_message)
            raise SyntaxError(error_message)

    def parse_variable_declaration(self):
        """Parse a variable declaration."""
        self.consume("Variable Declaration")  # I HAS A
        variable_name = self.current_token()[0]
        self.symbol_table[variable_name] = {"type": "NOOB", "value": "NOOB"}
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
            error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Variable '{variable_name}' not declared." # SAVE POINT
            if self.error_callback:
                self.error_callback(error_message)
            raise SyntaxError(error_message)
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
                error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Invalid type identifier: {new_type}" # SAVE POINT
                if self.error_callback:
                    self.error_callback(error_message)
                raise SyntaxError(error_message)
            self.consume("Type Identifier")
            self.symbol_table[variable_name]["type"] = new_type
            self.symbol_table[variable_name]["value"] = self.cast_value(self.symbol_table[variable_name]["value"], new_type)
        
        return self.symbol_table[variable_name]["value"]

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
                if self.current_token()[0] not in self.symbol_table:
                    error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Variable '{self.current_token()[0]}' not declared." # SAVE POINT
                    if self.error_callback:
                        self.error_callback(error_message)
                    raise SyntaxError(error_message) # SAVE POINT
                print("this is the current token",self.current_token()[0])
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
            if self.current_token() and self.current_token()[1] != "Linebreak":
                output.append(" ")
        self.IT = ''.join(map(str, output))
        print(f"VISIBLE: {self.IT}")
        if self.output_callback:
            self.output_callback(self.IT)
        self.consume("Linebreak")

    def parse_input(self):
        """Parse and execute a GIMMEH statement with a popup for input."""
        self.consume("Input Keyword")  # GIMMEH
        variable_name = self.current_token()[0]
        if variable_name not in self.symbol_table:
            error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Variable '{variable_name}' not declared." # SAVE POINT
            if self.error_callback:
                self.error_callback(error_message)
            raise SyntaxError(error_message)
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
        print("The input value is: ", input_value)
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
            error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Variable '{variable_name}' not declared." # SAVE POINT
            if self.error_callback:
                self.error_callback(error_message)
            raise SyntaxError(error_message)
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
        print("this is cond",condition)

        if self.current_token()[0] == "YA RLY":
            self.consume("Conditional Statement")
            self.consume("Linebreak")
            if condition == "WIN":
                while self.current_token() and self.current_token()[0] not in ["NO WAI", "OIC"]:
                    self.parse_statement()
                    if self.current_token() and self.current_token()[0] == "NO WAI" or self.current_token() and self.current_token()[0] == "OIC":
                        break
                # Skip NO WAI
                if self.current_token() and self.current_token()[0] == "NO WAI":
                    while self.current_token() and self.current_token()[0] != "OIC":
                        self.consume()
                # Still consume the OIC         
                self.consume("Conditional Statement")
                self.consume("Linebreak")
            else:
                # if condition is not met, then we directly go to NO WAI, or if there is NO WAI then go until OIC
                while self.current_token() and self.current_token()[0] not in ["NO WAI", "OIC"]:
                    self.consume()
                if self.current_token() and self.current_token()[0] == "NO WAI":
                    self.consume("Conditional Statement")
                    self.consume("Linebreak")
                    while self.current_token() and self.current_token()[0] != "OIC":
                        self.parse_statement()
                if self.current_token() and self.current_token()[0] == "OIC":
                    self.consume("Conditional Statement")
                    self.consume("Linebreak")

    def parse_loop(self):
        """Parse a loop construct (IM IN YR)."""
        self.consume("Loop Start")  # IM IN YR
        label = self.current_token()[0]
        self.consume("Variable Identifier")
        operation = self.current_token()[0]  # UPPIN or NERFIN
        self.consume("Loop Operation")
        self.consume("Construct")  # YR
        variable = self.current_token()[0] # num2
        print(f"variable: {variable}")
        self.consume("Variable Identifier")

        # loop statement is optional (til or wile)
        if self.current_token()[1] == "Loop Statement":
            condition_type = self.current_token()[0] # TIL OR WILE
            self.consume("Loop Statement")
            condition_cursor = self.cursor
            self.parse_expression() # di ata kelangan iparse to (?) kahit consume na lang siguro

            
        while True:
            # iccheck condition every time magloop 
            self.cursor = condition_cursor #temporarily put cursor here to parse expression
            if condition_type == "WILE":
                result = self.parse_expression()
                if result == "FAIL":
                    # we consume until we go to the end (since we backtracked)
                    while self.current_token() and self.current_token()[1] != "Loop End":
                        self.consume()
                    break
            
            elif condition_type == "TIL":
                result = self.parse_expression()
                if result == "WIN":
                    # we consume until we go to the end (since we backtracked)
                    while self.current_token() and self.current_token()[1] != "Loop End":
                        self.consume()
                    break

            print("ito yung cursor mo after mo gawen yung wile til: ", self.current_token())
            while self.current_token() and self.current_token()[1] != "Loop End":
                self.parse_statement()
            if operation == "UPPIN":
                self.symbol_table[variable].update({"value": self.symbol_table[variable]["value"] + 1})
            elif operation == "NERFIN":
                self.symbol_table[variable].update({"value": self.symbol_table[variable]["value"] - 1})
        self.consume("Loop End")  # IM OUTTA YR
        self.consume("Variable Identifier")  # ll


    def parse_function(self): # JUST USE THIS FOR DECLARATOIN OF FUNCTION BECAUSE IT SKIPS THE PARSE STATEMENTS WITHIN THE FUNCTION (ONLY GETS THE FUNCTION NAME AND PARAMETERS)
        """Parse a function definition (HOW IZ I)."""
        # print("this is the current value of cursor",self.cursor) TRACKERS
        self.consume("Function Start")  # HOW IZ I
        function_name = self.current_token()[0]
        self.function_locations[function_name] = self.cursor - 1
        # print("this is the function locations",self.function_locations) TRACKERS
        self.consume("Variable Identifier")
        parameters = []
        if self.current_token()[1] == "Construct":
            self.consume("Construct")
            parameters.append(self.current_token()[0])
            print("this is ",parameters)
            self.consume("Variable Identifier")
            while self.current_token()[1] == "Operator Separator":
                self.consume("Operator Separator")
                self.consume("Construct")
                parameters.append(self.current_token()[0])
                self.consume("Variable Identifier")
        self.consume("Linebreak")
        # STORE THE FUNCTION LOCATION
        while self.current_token() and self.current_token()[1] != "Function End":
            self.consume()
        self.consume("Function End")  # IF U SAY SO
        function_holder = {function_name: {param: None for param in parameters}}
        self.list_of_functions.append(function_holder)
        print("this is the list of functions",self.list_of_functions)

    
    def get_function_parameters(self, function_name):
        """Get the parameters of a function by its name."""
        for function in self.list_of_functions:
            if function_name in function:
                return function[function_name]
        return None

    # CHECK IF FUNCTION CALL IS VALID
    def check_function_call(self, function_name, args):
        """Check if the function call is valid."""
        parameters = self.get_function_parameters(function_name)
        if parameters is None:
            print(f"Function '{function_name}' not found.")
            return False
        if len(args) != len(parameters):
            print(f"Function '{function_name}' expects {len(parameters)} arguments, but got {len(args)}.")
            return False
        return True

    # PARSE FUNCTION CALL
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
        # CHECK VALIDITY OF FUNCTION CALL BEFORE GOING TO FUNCTION BLOCK
        if self.check_function_call(function_name, arguments):
            print("this arethe arguments",arguments)
            print("Function call successful.")
            self.function_block(function_name, arguments)
        else:
            error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Invalid function call: {function_name}({arguments})" # SAVE POINT
            if self.error_callback:
                self.error_callback(error_message)
            raise SyntaxError(error_message)

    
    def function_block(self, function_name, parameters):
        # THINGS TO RESET AFTER FUNCTION BLOCK
        temp_list_of_functions = self.list_of_functions.copy()
        temp_symbol_table = self.symbol_table.copy()
        temp_cursor = self.cursor
        self.cursor = self.function_locations[function_name]
        print("this is the cursor",self.cursor)
        print("symbol table before",self.symbol_table)
        GTFO_flag = False
        """Parse the block of a function."""
        print(f"Expecting Function Start, current token: {self.current_token()}")
        self.consume("Function Start")  # HOW IZ I 
        self.consume("Variable Identifier")

        # Retrieve the function from the list
        function = self.get_function_parameters(function_name)
        if function is None:
            error_message = f"Error occurred at line {self.current_line}.\n Value Error: Function '{function_name}' not found." # SAVE POINT
            if self.error_callback:
                self.error_callback(error_message)
            raise ValueError(error_message)
        
        # Initialize list_of_functions with function parameters
        self.list_of_functions = {param: {"type": None, "value": None} for param in function.keys()}
        print("this is the current list of functions",self.list_of_functions)
        
        # Update the function parameters with the provided values
        for param, value in zip(function.keys(), parameters):
            self.list_of_functions[param]["type"] = self.determine_type(value)
            self.list_of_functions[param]["value"] = value
        
        # Clear the symbol table and update it with the function parameters
        self.symbol_table.clear()
        self.symbol_table.update({param: {"type": self.list_of_functions[param]["type"], "value": self.list_of_functions[param]["value"]} for param in self.list_of_functions})
        
        self.symbol_table.update({'IT': {"type": "NOOB", "value": "NOOB"}})
        temp_symbol_table.update({'IT': {"type": "NOOB", "value": "NOOB"}})
        print("this is the symbol table",self.symbol_table)

        if self.current_token()[1] == "Construct":
            self.consume("Construct")
            self.consume("Variable Identifier")
            while self.current_token()[1] == "Operator Separator":
                self.consume("Operator Separator")
                self.consume("Construct")
                self.consume("Variable Identifier")
        self.consume("Linebreak")
        while self.current_token() and self.current_token()[1] != "Function End":
            print("this is the current token",self.current_token())
            if self.current_token()[1] == "Break/Return":
                self.consume("Break/Return")
                self.consume("Linebreak")
                GTFO_flag = True
                break
            if self.current_token()[1] == "Return":
                self.consume("Return")
            self.parse_statement()
            self.symbol_table['IT'] = {"type": self.determine_type(self.IT), "value": self.IT}
            temp_symbol_table['IT'] = {"type": self.determine_type(self.IT), "value": self.IT}
        self.consume("Function End")  # IF U SAY SO
        if GTFO_flag:
            temp_symbol_table.update({'IT': {"type": "NOOB", "value": "NOOB"}})
        self.cursor = temp_cursor
        self.list_of_functions = temp_list_of_functions
        print("this is list of function after",self.list_of_functions)
        self.symbol_table = temp_symbol_table
        print("this is the symbol table after",self.symbol_table)

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
            error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Unexpected token: {self.current_token()[0]}" # SAVE POINT
            if self.error_callback:
                self.error_callback(error_message)
            raise SyntaxError(error_message)

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
            error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Unexpected boolean operator: {operator}" # SAVE POINT
            if self.error_callback:
                self.error_callback(error_message)
            raise SyntaxError(error_message)

    def parse_literal_or_variable(self):
        """Parse a literal or variable."""
        if self.current_token()[1] == "String Delimiter":
            return self.parse_literal()
        elif self.current_token()[1] == "Literal":
            return self.parse_literal()
        elif self.current_token()[1] == "Variable Identifier":
            return self.parse_variable()
        else:
            error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Unexpected token: {self.current_token()[0]}" # SAVE POINT
            if self.error_callback:
                self.error_callback(error_message)
            raise SyntaxError(error_message)

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
            error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Unexpected literal at token '{self.current_token()[0]}'." # SAVE POINT
            if self.error_callback:
                self.error_callback(error_message)
            raise SyntaxError(error_message)

    def perform_arithmetic(self, left, right, operator):
        """Perform arithmetic based on the operator."""
        # print("this is ",right)
        if type(left) == str or type(left) == bool:
            left = self.cast_to_number(left)
        if type(right) == str or type(right) == bool:
            right = self.cast_to_number(right)
        # Ensure that left and right are numbers
        if isinstance(left, str):
            try:
                left = float(left) if '.' in left else int(left)
            except ValueError:
                error_message = f"Error occurred at line {self.current_line}.\n Type Error: Invalid operand type for arithmetic: {left}" # SAVE POINT
                if self.error_callback:
                    self.error_callback(error_message)
                raise TypeError(error_message)
        if isinstance(right, str):
            print("inside here")
            try:
                right = float(right) if '.' in right else int(right)
            except ValueError:
                error_message = f"Error occurred at line {self.current_line}.\n Type Error: Invalid operand type for arithmetic: {right}" # SAVE POINT
                if self.error_callback:
                    self.error_callback(error_message)
                raise TypeError(error_message)

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
            error_message = f"Error occurred at line {self.current_line}.\n Value Error: Unknown operator: {operator}" # SAVE POINT
            if self.error_callback:
                self.error_callback(error_message)
            raise ValueError(error_message)

    def parse_comparison(self):
        """Parse comparison operations and set a flag if the right side is nested."""
        operator = self.current_token()[0]
        self.consume("Comparison Operation")
        left = str(self.parse_expression())
        self.consume("Operator Separator")  # AN
        right = str(self.parse_expression())
        if operator == "BOTH SAEM":
            return "WIN" if left == right else "FAIL"
        elif operator == "DIFFRINT":
            return "WIN" if left != right else "FAIL"
    
        error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Unexpected comparison operator: {operator}" # SAVE POINT
        if self.error_callback:
            self.error_callback(error_message)
        raise SyntaxError(error_message)

    def parse_variable(self):
        """Parse and return the value of a variable."""
        var_name = self.current_token()[0]
        if var_name not in self.symbol_table:
            error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Variable '{var_name}' not declared." # SAVE POINT
            if self.error_callback:
                self.error_callback(error_message)
            raise SyntaxError(error_message)
        self.consume("Variable Identifier")
        return self.symbol_table[var_name]["value"]

    def parse_case(self):
        """Parse a case block."""
        omgwtf_flag = False
        condition = self.IT
        self.consume("Case Statement") # WTF?
        self.consume("Linebreak")
        while self.current_token():
            flag = False # reset the flag, so other cases will be checked
            if self.current_token()[0] == "OMG":

                self.consume("Case Statement") # OMG 
                # we get the literal to compare with condition
                switch_case = str(self.parse_literal()) # no. (e.g: OMG 1, OMG 2, OMG 3...)
                if condition == switch_case:
                    omgwtf_flag = True # if there is a time that one OMG switch case got true, then we set the flag to true
                # if the literal is the same as the condition
                self.consume("Linebreak")
                while self.current_token() and self.current_token()[0] not in ["GTFO", "OMGWTF"]:
                    if condition == switch_case:
                        self.parse_statement()
                    else:
                        self.consume()
                if self.current_token() and self.current_token()[0] == "OMGWTF": # serves as the wildcard (e.g: _)
                    self.consume("Case Statement")
                    self.consume("Linebreak")
                    # contents inside OMGWTF
                    while self.current_token() and self.current_token()[0] != "OIC":
                        # if one of the cases has been successfully executed, then we do not need to execute OMGWTF (default case)
                        if omgwtf_flag:
                            self.consume()
                        else:
                            self.parse_statement()
                    self.consume("Conditional Statement")
                    self.consume("Linebreak")
                    # we now get out of the codeblock if we encountered OIC
                    return
                # if token is not OMGWTF, or it is a normal OMG and Literal Combination (with a GTFO delimiter)
                self.consume("Break/Return")
                self.consume("Linebreak")
            else:
                error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Error while parsing case statement. Expected 'OMG'." # SAVE POINT
                if self.error_callback:
                    self.error_callback(error_message)
                raise SyntaxError(error_message)
                
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
                error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Cannot cast value '{value}' to NUMBR" # SAVE POINT
                if self.error_callback:
                    self.error_callback(error_message)
                raise SyntaxError(error_message)
        elif target_type == "NUMBAR":
            try:
                return float(value)
            except ValueError:
                error_message = f"Error occurred at line {self.current_line}.\n Syntax Error: Cannot cast value '{value}' to NUMBAR" # SAVE POINT
                if self.error_callback:
                    self.error_callback(error_message)
                raise SyntaxError(error_message)
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
            error_message = f"Error occurred at line {self.current_line}.\n Value Error: Invalid type casting to {target_type}" # SAVE POINT
            if self.error_callback:
                self.error_callback(error_message)
            raise ValueError(error_message)

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
                error_message = f"Error occurred at line {self.current_line}.\n Type Error: Cannot cast value to number: {value}" # SAVE POINT
                if self.error_callback:
                    self.error_callback(error_message)
                raise TypeError(error_message)

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