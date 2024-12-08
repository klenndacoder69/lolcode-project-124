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
            function_flag = False
            declare_flag = False
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

                    if declare_flag:
                        self.errors.append(f"Unexpected self.current_token() '{self.current_token()[0]}'.")
                        raise SyntaxError("Error while parsing declare variables. Only one declare variables block is allowed.")
                    
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
                    declare_flag = True
                    function_flag = True

                elif self.current_token()[1] == "Input Keyword":  # GIMMEH always uses a variable
                    self.consume("Input Keyword")
                    self.consume("Variable Identifier")
                    self.check_for_valid_inline_comments()
                    self.consume("Linebreak")

                elif self.current_token()[1] == "Output Keyword":  # VISIBLE
                    self.parse_output()
                elif self.current_token()[1] in ["Arithmetic Operation", "Comparison Operation", "Boolean Operation"]: 
                    self.parse_expression()
                    self.consume("Linebreak")
                    # handle the conditional statements
                    if self.current_token() and self.current_token()[0] == "O RLY?":
                        self.consume("Conditional Statement")
                        self.check_for_valid_inline_comments()
                        self.consume("Linebreak")
                        # check if the next token is YA RLY
                        if self.current_token() and self.current_token()[0] == "YA RLY":

                            self.consume("Conditional Statement")
                            self.check_for_valid_inline_comments()
                            self.consume("Linebreak")
                            print(self.current_token())
                            # NO WAI is optional, but we still check it. We check for NO WAI and OIC
                            while self.current_token() and self.current_token()[0] not in ["NO WAI", "OIC"]:
                                self.consume() # we consume each thing inside the o rly thing

                            if self.current_token() and self.current_token()[0] == "NO WAI": # if no wai is present, then we check until oic
                                self.consume("Conditional Statement")
                                self.check_for_valid_inline_comments()
                                self.consume("Linebreak")
                                while self.current_token() and self.current_token()[0] != "OIC":
                                    self.consume()
                            if self.current_token() and self.current_token()[0] == "OIC": # however if no wai is not present, then we check oic directly
                                self.consume("Conditional Statement")
                                self.check_for_valid_inline_comments()
                                self.consume("Linebreak")                   
                    else:
                        print (f"Bad loop lods '{self.current_token()[1]}'.")
                        raise SyntaxError(f"Bad loop lods '{self.current_token()[0]}'.")

                elif self.current_token()[1] == "Variable Identifier": # R (variable assignment)
                    self.consume("Variable Identifier")
                    if self.current_token()[1] == "Variable Assignment":
                        self.consume("Variable Assignment") # R 10, R SMOOSH, R MAEK
                        if self.current_token() and self.current_token()[1] == "Literal":
                            self.parse_expression()
                        elif self.current_token() and self.current_token()[1] == "String Concatenation":
                            self.parse_smoosh()
                        elif self.current_token() and self.current_token()[1] == "Typecasting": # MAEK
                            self.consume("Typecasting")
                            self.consume("Typecasting")
                            self.consume("Variable Identifier")
                            self.consume("Type Identifier")
                            self.check_for_valid_inline_comments()
                    elif self.current_token()[1] == "Typecasting": # IS NOW A or MAEK
                        self.consume("Typecasting")
                        self.consume("Type Identifier")
                        self.check_for_valid_inline_comments()

                elif self.current_token()[0] == "WTF?":
                    self.consume("Case Statement")
                    self.check_for_valid_inline_comments()
                    self.consume("Linebreak")
                    
                    while self.current_token():

                        if self.current_token()[0] == "OMG":

                            self.consume("Case Statement") # OMG 
                            self.consume("Literal") # no. (e.g: OMG 1, OMG 2, OMG 3...)
                            self.check_for_valid_inline_comments()
                            self.consume("Linebreak")
                            while self.current_token() and self.current_token()[0] not in ["GTFO", "OMGWTF"]:
                                print("\nThis is the current token:", self.current_token())
                                self.consume()
                            if self.current_token() and self.current_token()[0] == "OMGWTF": # serves as the wildcard (e.g: _)
                                self.consume("Case Statement")
                                self.check_for_valid_inline_comments()
                                self.consume("Linebreak")
                                # contents inside OMGWTF
                                while self.current_token() and self.current_token()[0] != "OIC":
                                    self.parse_valid_code_block()
                                self.consume("Conditional Statement")
                                self.check_for_valid_inline_comments()
                                self.consume("Linebreak")
                                break
                            # if token is not OMGWTF, or it is a normal OMG and Literal Combination (with a GTFO delimiter)
                            self.consume("Break/Return")
                            self.check_for_valid_inline_comments()
                            self.consume("Linebreak")
                        else:
                            raise SyntaxError("Error while parsing case statement. Expected 'OMG'.")
                
                elif self.current_token()[1] == "Loop Start":
                    self.consume("Loop Start") # im in yr
                    self.consume("Variable Identifier") # <label>
                    self.consume("Loop Operation") # uppin  (operation)
                    self.consume("Construct") # yr
                    self.consume("Variable Identifier") # variable
                    if self.current_token() and self.current_token()[1] == "Loop Statement":
                        # til|wile <expression> is optional
                        self.consume("Loop Statement") # til|wile
                        self.parse_expression() # expression
                        
                    while self.current_token() and self.current_token()[1] != "Loop End":
                        self.parse_valid_code_block()
                    self.consume("Loop End") # im outta yr
                    self.consume("Variable Identifier") # <label>
                    self.check_for_valid_inline_comments() # chk for inline comments
                    self.consume("Linebreak")

                elif self.current_token()[1] == "Function Start":
                    if function_flag:
                        raise SyntaxError("Functions are only allowed to be declared before the variable declaration block.")
                    self.consume("Function Start") # how iz i
                    self.consume("Variable Identifier") # variable name <label>
                    # this part is optional, as a function may have no parameters
                    if self.current_token() and self.current_token()[1] == "Linebreak":
                        self.check_for_valid_inline_comments()
                        self.consume("Linebreak")
                    else:
                        # check for the first parameter (as first parameter does not need an AN, and only one YR)
                        # having a construct may be optional (?)
                        # if self.current_token() and self.current_token()[1] == "Construct":  (removed based on recent corrections)
                        self.consume("Construct")
                        self.consume("Variable Identifier")
                        # for the rest of the parameters
                        # AN YR may be optional (?)
                        while self.current_token() and self.current_token()[1] != "Linebreak":
                            # if self.current_token() and self.current_token()[1] == "Operator Separator": (removed based on recent corrections)
                            self.consume("Operator Separator") # AN
                            self.consume("Construct") # YR
                            self.consume("Variable Identifier") # <variable>
                        self.check_for_valid_inline_comments()
                        self.consume("Linebreak")
                    # function body
                    # function body may end with either a FOUND YR, a GTFO, or directly to IF U SAY SO (only one can exist (?))
                    while self.current_token() and self.current_token()[1] not in ["Function End", "Return", "Break/Return"]:
                        self.parse_valid_code_block()
                    if self.current_token() and self.current_token()[1] == "Return": # FOUND YR
                        self.consume("Return")
                        self.parse_expression()
                        self.check_for_valid_inline_comments()
                        self.consume("Linebreak")
                    elif self.current_token() and self.current_token()[1] == "Break/Return": # GTFO
                        self.consume("Break/Return")
                        self.check_for_valid_inline_comments()
                        self.consume("Linebreak")
                        
                    self.consume("Function End") # IF U SAY SO
                    self.check_for_valid_inline_comments() 
                    self.consume("Linebreak") 

                elif self.current_token()[1] == "Function Call":
                    self.consume("Function Call")
                    self.consume("Function Identifier")
                    # there are no parameters for the function call
                    if self.current_token() and self.current_token()[1] == "Arity Delimiter":
                        self.consume("Arity Delimiter")
                        self.check_for_valid_inline_comments()
                        self.consume("Linebreak")
                    else:
                        # if there is only one parameter for the function call
                        if self.current_token() and self.current_token()[1] == "Construct":
                            self.consume("Construct")
                        self.parse_expression()
                        # if there are multiple parameters for the function call
                        # MKAY might be optional (?)
                        while self.current_token() and self.current_token()[1] not in ["Arity Delimiter", "Linebreak"]: 
                            # if self.current_token() and self.current_token()[1] == "Operator Separator": (removed based on recent corrections)
                            self.consume("Operator Separator")
                            self.consume("Construct")
                            self.parse_expression()
                        # if there is an mkay (idk abt this)
                        if self.current_token() and self.current_token()[1] == "Arity Delimiter":
                            self.consume("Arity Delimiter") # consume the arity (MKAY)
                        self.check_for_valid_inline_comments()
                        self.consume("Linebreak")
                
                else:
                    self.errors.append(f"Unexpected self.current_token() '{self.current_token()[0]}'.")
                    raise SyntaxError(f"Note: Unexpected self.current_token() '{self.current_token()[0]}'.")
                
            self.consume("Ending Program")
            self.check_for_valid_inline_comments()
            print("Errors:\n", self.errors)
            print("Program is syntactically correct.\n")
        except SyntaxError as e:
            print(f"Syntax Error: {e}")
    
    def parse_arithmetic(self):
        """Parse arithmetic operations."""
        if self.current_token()[1] in ["Arithmetic Operation", "Boolean Operation", "Comparison Operation"]:
            self.consume(self.current_token()[1])
            self.parse_arithmetic()  # Operand 1
            self.consume("Operator Separator")  # AN
            self.parse_arithmetic()  # Operand 2
        elif self.current_token()[1] in ["Literal", "Variable Identifier"]:
            self.consume(self.current_token()[1])

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
            while self.current_token() and self.current_token()[1] != "Ending Multiple Line Comment":
                self.consume()  # Consume each self.current_token() inside the comment
            if self.current_token()[1] == "Ending Multiple Line Comment":
                self.consume("Ending Multiple Line Comment")  # TLDR
                self.consume("Linebreak")  # Consume the linebreak after TLDR

    def parse_variable_declaration(self):
        """Parse a single variable declaration."""
        self.consume("Variable Declaration")  # I HAS A
        self.consume("Variable Identifier")  # Variable name
        if self.current_token() and self.current_token()[1] == "Variable Assignment":  # ITZ
            self.consume("Variable Assignment")
            self.parse_expression()
    def parse_smoosh(self):
        self.consume("String Concatenation")
        # This is needed as SMOOSH are not able to have a logical expression
        while self.current_token() and self.current_token()[1] != "Linebreak":
            if self.current_token()[1] in ["Literal", "String Delimiter"]:
                self.parse_literal()
            elif self.current_token()[1] == "Variable Identifier":
                self.consume("Variable Identifier")
            elif self.current_token()[1] == "Operator Separator":
                self.consume("Operator Separator")
            elif self.current_token()[1] == "Single Line Comment":
                self.check_for_valid_inline_comments()
            else:
                self.errors.append(f"Unexpected self.current_token() '{self.current_token()[0]}'.")
                raise SyntaxError("Error while parsing string concatenation. Logical expressions are not allowed.")
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
                self.parse_smoosh()
                # we return  since we did the loop here
                return
            elif self.current_token()[1] == "Operator":
                self.consume("Operator")
                self.parse_expression()
                continue
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
        if self.current_token()[1] == "Arithmetic Operation":
            self.consume(self.current_token()[1])
            self.parse_expression()  # Operand 1
            self.consume("Operator Separator")  # AN
            self.parse_expression()  # Operand 2

            
        elif self.current_token()[1] == "Comparison Operation":
            if self.current_token()[0] in ["BOTH SAEM", "DIFFRINT"]:
                self.consume("Comparison Operation")
                self.parse_expression()  # Operand 1
                self.consume("Operator Separator")  # AN
                self.parse_expression()  # Operand 2
        elif self.current_token()[1] == "Boolean Operation":
            if self.current_token()[0] == "NOT":
                self.consume("Boolean Operation")
                self.parse_expression() # Operand 1 for NOT
            if self.current_token()[0] in ["BOTH OF", "EITHER OF", "WON OF"]:
                self.consume("Boolean Operation")
                self.parse_expression()  # Operand 1
                self.consume("Operator Separator")  # AN
                self.parse_expression()  # Operand 2
            if self.current_token()[0] in ["ALL OF", "ANY OF"]:
                self.consume("Boolean Operation")
                self.parse_expression()
                # There are infinite operands, so we must create a while loop
                while self.current_token() and self.current_token()[1] != "Arity Delimiter":
                    self.consume("Operator Separator")
                    self.parse_expression()
                self.consume("Arity Delimiter")
        elif self.current_token()[1] in ["Literal", "Variable Identifier", "String Delimiter"]:
            if self.current_token()[1] == "String Delimiter":
                self.parse_literal()
            else:
                # if not a string delimiter
                self.consume(self.current_token()[1])
        elif self.current_token()[1] == "Single Line Comment":
            # We must check only when the next self.current_token() is a linebreak
            self.check_for_valid_inline_comments()

        else:
            self.errors.append(f"Invalid expression at self.current_token() '{self.current_token()[0]}'.")
            raise SyntaxError(f"Note: Invalid expression at self.current_token() '{self.current_token()[0]}'.")

    # this is for code blocks
    def parse_valid_code_block(self):
        if self.current_token()[1] == "Linebreak":
                    self.consume("Linebreak")

        elif self.current_token()[1] == "Single Line Comment" or self.current_token()[1] == "Starting Multiple Line Comment":
            self.parse_comments()
        elif self.current_token()[1] == "Input Keyword":  # GIMMEH always uses a variable
                    self.consume("Input Keyword")
                    self.consume("Variable Identifier")
                    self.check_for_valid_inline_comments()
                    self.consume("Linebreak")

        elif self.current_token()[1] == "Output Keyword":  # VISIBLE
            self.parse_output()
        elif self.current_token()[1] in ["Arithmetic Operation", "Comparison Operation", "Boolean Operation"]: 
            self.parse_expression()
            self.consume("Linebreak")
            # handle the conditional statements
            if self.current_token() and self.current_token()[0] == "O RLY?":
                self.consume("Conditional Statement")
                self.check_for_valid_inline_comments()
                self.consume("Linebreak")
                # check if the next token is YA RLY
                if self.current_token() and self.current_token()[0] == "YA RLY":

                    self.consume("Conditional Statement")
                    self.check_for_valid_inline_comments()
                    self.consume("Linebreak")
                    print(self.current_token())
                    # NO WAI is optional, but we still check it. We check for NO WAI and OIC
                    while self.current_token() and self.current_token()[0] not in ["NO WAI", "OIC"]:
                        self.parse_valid_code_block() # we consume each thing inside the o rly thing

                    if self.current_token() and self.current_token()[0] == "NO WAI": # if no wai is present, then we check until oic
                        self.consume("Conditional Statement")
                        self.check_for_valid_inline_comments()
                        self.consume("Linebreak")
                        while self.current_token() and self.current_token()[0] != "OIC":
                            self.parse_valid_code_block()
                    if self.current_token() and self.current_token()[0] == "OIC": # however if no wai is not present, then we check oic directly
                        self.consume("Conditional Statement")
                        self.check_for_valid_inline_comments()
                        self.consume("Linebreak")                   
            else:
                print (f"Bad loop lods '{self.current_token()[1]}'.")
                raise SyntaxError(f"Bad loop lods '{self.current_token()[0]}'.")

        elif self.current_token()[1] == "Variable Identifier": # R (variable assignment)
            self.consume("Variable Identifier")
            if self.current_token()[1] == "Variable Assignment":
                self.consume("Variable Assignment") # R 10, R SMOOSH, R MAEK
                if self.current_token() and self.current_token()[1] == "Literal":
                    self.parse_expression()
                elif self.current_token() and self.current_token()[1] == "String Concatenation":
                    self.parse_smoosh()
                elif self.current_token() and self.current_token()[1] == "Typecasting": # MAEK
                    self.consume("Typecasting")
                    self.consume("Variable Identifier")
                    self.consume("Type Identifier")
                    self.check_for_valid_inline_comments()
            elif self.current_token()[1] == "Typecasting": # IS NOW A or MAEK
                self.consume("Typecasting")
                self.consume("Type Identifier")
                self.check_for_valid_inline_comments()

        elif self.current_token()[0] == "WTF?":
            self.consume("Case Statement")
            self.check_for_valid_inline_comments()
            self.consume("Linebreak")
            
            while self.current_token():

                if self.current_token()[0] == "OMG":

                    self.consume("Case Statement") # OMG 
                    self.consume("Literal") # no. (e.g: OMG 1, OMG 2, OMG 3...)
                    self.check_for_valid_inline_comments()
                    self.consume("Linebreak")
                    while self.current_token() and self.current_token()[0] not in ["GTFO", "OMGWTF"]:
                        print("\nThis is the current token:", self.current_token())
                        self.parse_valid_code_block()
                    if self.current_token() and self.current_token()[0] == "OMGWTF": # serves as the wildcard (e.g: _)
                        self.consume("Case Statement")
                        self.check_for_valid_inline_comments()
                        self.consume("Linebreak")
                        # contents inside OMGWTF
                        while self.current_token() and self.current_token()[0] != "OIC":
                            self.parse_valid_code_block()
                        self.consume("Conditional Statement")
                        self.check_for_valid_inline_comments()
                        self.consume("Linebreak")
                        break
                    # if token is not OMGWTF, or it is a normal OMG and Literal Combination (with a GTFO delimiter)
                    self.consume("Break/Return")
                    self.check_for_valid_inline_comments()
                    self.consume("Linebreak")
                else:
                    raise SyntaxError("Error while parsing case statement. Expected 'OMG'.")
        
        elif self.current_token()[1] == "Loop Start":
            self.consume("Loop Start") # im in yr
            self.consume("Variable Identifier") # <label>
            self.consume("Loop Operation") # uppin  (operation)
            self.consume("Construct") # yr
            self.consume("Variable Identifier") # variable
            if self.current_token() and self.current_token()[1] == "Loop Statement":
                # til|wile <expression> is optional
                self.consume("Loop Statement") # til|wile
                self.parse_expression() # expression
                
            while self.current_token() and self.current_token()[1] != "Loop End":
                self.consume()
            self.consume("Loop End") # im outta yr
            self.consume("Variable Identifier") # <label>
            self.check_for_valid_inline_comments() # chk for inline comments
            self.consume("Linebreak")
            
        elif self.current_token()[1] == "Function Call":
                    self.consume("Function Call")
                    self.consume("Function Identifier")
                    # there are no parameters for the function call
                    if self.current_token() and self.current_token()[1] == "Arity Delimiter":
                        self.consume("Arity Delimiter")
                        self.check_for_valid_inline_comments()
                        self.consume("Linebreak")
                    else:
                        # if there is only one parameter for the function call
                        if self.current_token() and self.current_token()[1] == "Construct":
                            self.consume("Construct")
                        self.parse_expression()
                        # if there are multiple parameters for the function call
                        # MKAY might be optional (?)
                        while self.current_token() and self.current_token()[1] not in ["Arity Delimiter", "Linebreak"]: 
                            # if self.current_token() and self.current_token()[1] == "Operator Separator": (removed based on recent corrections)
                            self.consume("Operator Separator")
                            self.consume("Construct")
                            self.parse_expression()
                        # if there is an mkay (idk abt this)
                        if self.current_token() and self.current_token()[1] == "Arity Delimiter":
                            self.consume("Arity Delimiter") # consume the arity (MKAY)
                        self.check_for_valid_inline_comments()
                        self.consume("Linebreak")
        else:
            self.errors.append(f"Unexpected self.current_token() '{self.current_token()[0]}'.")
            raise SyntaxError(f"Note: Unexpected self.current_token() '{self.current_token()[0]}'.")