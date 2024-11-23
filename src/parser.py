class Parser:
    def __init__(self, lexemes):
        """
        Initialize the syntax analyzer with the lexemes.
        lexemes: List of tuples, where each tuple contains a lexeme and its classification.
        """
        self.lexemes = lexemes
        self.cursor = 0
        self.errors = []

    def current_token(self):
        """Return the current self.current_token() as a tuple or None if out of bounds."""
        return self.lexemes[self.cursor] if self.cursor < len(self.lexemes) else None

    def consume(self, expected_type=None):
        """
        Consume the current self.current_token() if it matches the expected type.
        Raise a syntax error if the self.current_token() does not match.
        """
        # if self.current_token() and self.current_token()[1] == "Single Line Comment":
        #     if self.lexemes[self.cursor + 1][1] == "Linebreak":
        #         self.cursor += 1
        if self.current_token() is None:
            raise SyntaxError(f"Unexpected end of input.")
        if expected_type is None or self.current_token()[1] == expected_type:
            print(f"Consuming token: {self.current_token()[0]} with Classification: {self.current_token()[1]}")
            self.cursor += 1
            return self.current_token()
        raise SyntaxError(f"Expected {expected_type}, got {self.current_token()[1]} at self.current_token() '{self.current_token()[0]}'.")
    def check_for_valid_inline_comments(self):
        if self.current_token()[1] == "Single Line Comment":
            if self.lexemes[self.cursor + 1][1] == "Linebreak":
                self.consume("Single Line Comment")
    def parse_program(self):
        """Parse the entire program."""
        try:
            # Handle comments outside Starting Program
            multi_flag = False
            while self.current_token():
                if self.current_token()[1] == "Starting Program":
                    break  # Begin parsing program after this self.current_token()
                
                # Handle comments
                if self.current_token()[1] == "Linebreak":
                    self.consume("Linebreak")

                elif self.current_token()[1] == "Single Line Comment":
                    self.consume("Single Line Comment")

                elif self.current_token()[1] == "Starting Multiple Line Comment":
                    multi_flag = True
                    self.consume("Starting Multiple Line Comment")

                elif self.current_token()[1] == "Ending Multiple Line Comment" and multi_flag:
                    multi_flag = False
                    self.consume("Ending Multiple Line Comment")

                else:
                    # Handle unexpected tokens
                    self.errors.append(f"Unexpected self.current_token() '{self.current_token()[0]}'.")
            
            self.consume("Starting Program")  # HAI
            self.check_for_valid_inline_comments()
            self.consume("Linebreak")
            
            # MAIN LOOP OF THE PROGRAM --------
            while self.current_token() and self.current_token()[1] != "Ending Program":

                if self.current_token()[1] == "Linebreak":
                    self.consume("Linebreak")

                elif self.current_token()[1] == "Single Line Comment" or self.current_token()[1] == "Starting Multiple Line Comment":
                    self.parse_comments()

                # DECLARING VARIABLES --------------
                elif self.current_token()[1] == "Starting Declare Variables":
                    self.consume("Starting Declare Variables")  # WAZZUP

                    self.check_for_valid_inline_comments()

                    self.consume("Linebreak") 
                    # LOOP FRO DECLARING VARIABLES
                    while self.current_token() and self.current_token()[1] != "Ending Declare Variables":
                        # print(self.current_token())

                        if self.current_token()[1] == "Ending Declare Variables": #BUHBYE
                            self.consume("Ending Declare Variables")

                            self.check_for_valid_inline_comments()

                            break
                        if self.current_token()[1] == "Linebreak":
                            self.consume("Linebreak")

                        elif self.current_token()[1] == "Single Line Comment" or self.current_token()[1] == "Starting Multiple Line Comment":
                            self.parse_comments()

                        elif self.current_token()[1] == "Variable Declaration":
                            self.parse_variable_declaration()

                        else:
                            self.errors.append(f"Unexpected self.current_token() '{self.current_token()[0]}'.")
                            break
                    self.consume("Ending Declare Variables")  # BUHBYE

                elif self.current_token()[1] == "Input Keyword":  # GIMMEH always uses a variable
                    self.consume("Input Keyword")
                    self.consume("Variable Identifier")
                    self.check_for_valid_inline_comments()
                    self.consume("Linebreak")

                elif self.current_token()[1] == "Output Keyword":  # VISIBLE
                    self.parse_output()
                    pass
                else:
                    self.errors.append(f"Unexpected self.current_token() '{self.current_token()[0]}'.")
                    raise SyntaxError(f"Note: Unexpected self.current_token() '{self.current_token()[0]}'.")
            self.consume("Ending Program")
            self.check_for_valid_inline_comments()
            print("Errors:\n", self.errors)
            print("Program is syntactically correct.\n")
        except SyntaxError as e:
            print(f"Syntax Error: {e}")

    def parse_comments(self):
        """Parse comments before the program starts (HAI)."""
        if self.current_token()[1] == "Single Line Comment":
            # Single-line comment: Consume 'BTW' and the comment
            self.consume("Single Line Comment")
            self.consume("Linebreak")  # Consume the linebreak after the comment
        elif self.current_token()[1] == "Starting Multiple Line Comment":
            # Multi-line comment: Consume 'OBTW', process the comment, and end with 'TLDR'
            self.consume("Starting Multiple Line Comment")  # OBTW
            self.consume("Linebreak")  # Consume the linebreak after OBTW
            while self.current_token() and self.current_token()[0] != "TLDR":
                self.consume()  # Consume each self.current_token() inside the comment
            if self.current_token()[0] == "Ending Multiple Line Comment":
                self.consume("Ending Multiple Line Comment")  # TLDR
                self.consume("Linebreak")  # Consume the linebreak after TLDR

    def parse_variable_declaration(self):
        """Parse a single variable declaration."""
        self.consume("Variable Declaration")  # I HAS A
        self.consume("Variable Identifier")  # Variable name
        if self.current_token() and self.current_token()[1] == "Variable Assignment":  # ITZ
            self.consume("Variable Assignment")
            self.parse_expression()
    
    def parse_output(self):
        """Parse an output statement (VISIBLE)."""
        self.consume("Output Keyword")  # VISIBLE
        while self.current_token() and self.current_token()[1] != "Linebreak":
            if self.current_token()[1] == "Operator Separator":
                self.consume("Operator Separator")
                # I don't get why (VISIBLE "test" AN 12 AN) is possible. This line is solely the reason why I added this.
                # having SMOOSH needs to have an expression after AN
                if self.current_token()[1] == "Linebreak":
                    break
                self.parse_expression()
                continue
            elif self.current_token()[1] == "String Concatenation":
                self.consume("String Concatenation")
                # This is needed as SMOOSH are not able to have a logical expression
                while self.current_token() and self.current_token()[1] != "Linebreak":
                    if self.current_token()[1] in ["Literal", "String Delimiter"]:
                        self.parse_literal()
                    elif self.current_token()[1] == "Variable Identifier":
                        self.consume("Variable Identifier")
                    elif self.current_token()[1] == "Operator Separator":
                        self.consume("Operator Separator")
                    else:
                        self.errors.append(f"Unexpected self.current_token() '{self.current_token()[0]}'.")
                        raise SyntaxError("Error while parsing string concatenation. Logical expressions are not allowed.")
                return
            # keep parsing            
            self.parse_expression()
    def parse_literal(self):
        """Parse a literal which can be either a string or a number."""
        if self.current_token()[1] == "String Delimiter":
            self.consume("String Delimiter")
            self.consume("Literal")
            self.consume("String Delimiter")
        elif self.current_token()[1] == "Literal":
            self.consume("Literal")
        else:
            self.errors.append(f"Unexpected literal at token '{self.current_token()[0]}'.")
    def parse_expression(self):
        """Parse an expression."""
        if self.current_token()[1] in ["Arithmetic Operation", "Boolean Operation", "Comparison Operation"]:
            self.consume(self.current_token()[1])
            self.parse_expression()  # Operand 1
            self.consume("Operator Separator")  # AN
            self.parse_expression()  # Operand 2
        elif self.current_token()[1] in ["Literal", "Variable Identifier", "String Delimiter"]:
            if self.current_token()[1] == "String Delimiter":
                self.parse_literal()
            else:
                self.consume(self.current_token()[1])
        elif self.current_token()[1] == "Single Line Comment":
            # We must check only when the next self.current_token() is a linebreak
            self.check_for_valid_inline_comments()

        else:
            self.errors.append(f"Invalid expression at self.current_token() '{self.current_token()[0]}'.")
            raise SyntaxError(f"Note: Invalid expression at self.current_token() '{self.current_token()[0]}'.")




