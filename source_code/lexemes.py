
'''
Group: Detective Cunan1
Authors:
Klenn Jakek Borja
Shawn Clyde Diares
Kervin Ralph Samson

Section: ST1L
'''

import re
from tkinter import Tk, filedialog

# defined regular expression paterns

regex_patterns = {
    r'^HAI$': 'Starting Program',
    r'^KTHXBYE$': 'Ending Program',
    r'^I HAS A$': 'Variable Declaration', 
    r'^WAZZUP$' : 'Starting Declare Variables',
    r'^BUHBYE$' : 'Ending Declare Variables',
    r'^BTW$' : 'Single Line Comment',
    r'^OBTW$' : 'Starting Multiple Line Comment',
    r'^TLDR$' : 'Ending Multiple Line Comment',
    r'^ITZ$' : 'Variable Assignment',
    r'^R$' : 'Variable Assignment',
    r'^\+$' : 'Operator',
    r'^SUM OF$' : 'Arithmetic Operation',
    r'^DIFF OF$' : 'Arithmetic Operation',
    r'^PRODUKT OF$' : 'Arithmetic Operation',
    r'^QUOSHUNT OF$' : 'Arithmetic Operation',
    r'^MOD OF$' : 'Arithmetic Operation',
    r'^BIGGR OF$' : 'Arithmetic Operation',
    r'^SMALLR OF$' : 'Arithmetic Operation',
    r'^BOTH OF$' : 'Boolean Operation',
    r'^EITHER OF$' : 'Boolean Operation',
    r'^WON OF$' : 'Boolean Operation',
    r'^NOT$' : 'Boolean Operation',
    r'^ANY OF$' : 'Boolean Operation',
    r'^ALL OF$' : 'Boolean Operation',
    r'^BOTH SAEM$' : 'Comparison Operation',
    r'^DIFFRINT$' : 'Comparison Operation',
    r'^SMOOSH$' : 'String Concatenation',
    r'^MAEK$' : 'Typecasting',
    r'^AN$' : 'Operator Separator',
    r'^A$' : 'Typecasting',
    r'^IS NOW A$' : 'Typecasting',
    r'^VISIBLE$' : 'Output Keyword',
    r'^GIMMEH$' : 'Input Keyword',
    r'^O RLY\?$' : 'Conditional Statement',
    r'^YA RLY$' : 'Conditional Statement',
    r'^MEBBE$' : 'Conditional Statement',
    r'^NO WAI$' : 'Conditional Statement',
    r'^OIC$' : 'Conditional Statement',
    r'^WTF\?$' : 'Case Statement',
    r'^OMG$' : 'Case Statement',
    r'^OMGWTF$' : 'Case Statement',
    r'^IM IN YR$' : 'Loop Start',
    r'^UPPIN$' : 'Loop Operation',
    r'^NERFIN$' : 'Loop Operation',
    # this was changed, since YR is not necessarily for loops only, also for functions
    r'^YR$' : 'Construct',
    r'^TIL$' : 'Loop Statement',
    r'^WILE$' : 'Loop Statement',
    r'^IM OUTTA YR$' : 'Loop End',
    r'^HOW IZ I$' : 'Function Start',
    r'^IF U SAY SO$' : 'Function End',
    r'^GTFO$' : 'Break/Return',
    r'^FOUND YR$' : 'Return',
    r'^I IZ$' : 'Function Call',
    r'^MKAY$' : 'Arity Delimiter',
    r'\"': 'String Delimiter',
    r'^\n$': "Linebreak",
    # Identifier regex pattern, make sure this comes after specific cases like delimiters
    r'^(WIN|FAIL)$' : 'Literal',
    r'^(NOOB|NUMBA?R|YARN|TROOF)$' : 'Type Identifier',
    r'^([a-zA-Z][a-zA-Z0-9_]*)$': 'Variable Identifier',
    r'^(-?[1-9][0-9]*|0)$' : 'Literal',
    # Fixed pattern for floating-point literals
    r'^-?\d*\.\d+$' : 'Literal',  
    r'"[^"]*"|[^"\s]+' : 'Literal', 
    r'^([a-zA-Z][a-zA-Z0-9_]*\(.*\))$' : 'Function Identifier',
    r'^([a-zA-Z][a-zA-Z0-9_]*\(.*\))$' : 'Loop Identifier'
}

# Function to tokenize and match each token
def tokenize_and_match(line):
    '''
        Priority listings: 
        1. Multiword regexes - 1
        2. Quoted strings - 2
        3. String literals - 3
    '''
    
    '''
        Handle quoted strings and preserve them as one token
        This will match any quoted string and preserve it as a single token
    '''
    quoted_string_pattern = r'"[^"]*"|[^"\s]+'
    tokens = []
    
    
        #   This contains the multiword regexes (Multiword - highest priority)
    multiword_regexes = [regex[1:-1] for regex in regex_patterns.keys() if len(regex.split()) > 1]

    '''
        We match the string based on its priority list
        Find all quoted strings and add them to the tokens list
        Find all multiword strings and add them to the tokens list
    '''

        # Create a dictionary to store the placeholders for processing later(multiword strings)
    placeholders = {}
    placeholder_counter = 1

        # Loop to check all regular expressions of all the multiword regexes
    for regex in multiword_regexes:

        for match in re.finditer(regex, line):
            
            # Replace the matched string with a placeholder
            placeholder = f"_multiword_{placeholder_counter}"
            line = line.replace(match.group(0), placeholder, 1)

            # Add placeholder to dictionary
            placeholders[placeholder] = match.group(0)
            placeholder_counter += 1

        #   This loop checks for quoted strings and adds them to the tokens list
    for match in re.finditer(quoted_string_pattern, line):
        if(match.group(0).startswith('"') and match.group(0).endswith('"')):

                #   Append the opening and closing double quotes
            tokens.append("\"")
            tokens.append(match.group(0))
            tokens.append("\"")
            continue
            
            #   If line starts with BTW or OBTW or TLDR, append it to the tokens list (however, ignore the rest of the line)
        if(match.group(0) == "BTW" or match.group(0) == "OBTW" or match.group(0) == "TLDR"):
                tokens.append(match.group(0))
                break
        tokens.append(match.group(0))
    

    '''
        Step 3: Match each token with the regex patterns
        This array contains the substituted multiwords
    '''
    matched_tokens = []
        # This for loop iterates over each token with a quotation mark which indicates a string literal
    for token in tokens:

            # Bool flag to check if a match is found
        matched = False

        for pattern, category in regex_patterns.items(): # pattern = key , category = value
                # Check if the token matches the pattern ( e.g: ^(WIN|FAIL)$' )
            if re.fullmatch(pattern, token): # dapat exact 

                    # If category is a string literal, then we remove its quotes and print
                
                if category == "Literal" and token.startswith('"') and token.endswith('"'):
                    x = slice(1,-1)

                    # Note: To avoid confusion, we just appended the strings containing the token and its classifications inside the matched_tokens array
                    matched_tokens.append(f"Lexeme` {token[x]} -> Classification` {category}")
                    matched = True
                    break
                
                    # If it is not a string literal, it immediately appends
                matched_tokens.append(f"Lexeme` {token} -> Classification` {category}")
                matched = True
                break  # Stop checking once a match is found

        if not matched:
            matched_tokens.append(f"No match for: {token}")

        # Replace the multiwords with its original names (which is indicated by the placeholders dictionary)
        # This indicates that the statement after a function category is a function identifier
    next_token_is_fnc_id = False
    next_token_is_loop_id = False
    final_tokens = []
        # The sole purpose of this for loop is to check whether the matched tokens are function/loop identifiers
    for matched_token in matched_tokens:
        if next_token_is_loop_id:
            final_tokens.append(f"Lexeme` {matched_token.split("`")[1].strip()} ` Loop Identifier")
            next_token_is_loop_id = False
            continue
        if next_token_is_fnc_id:
            final_tokens.append(f"Lexeme` {matched_token.split("`")[1].strip()} ` Function Identifier")
            next_token_is_fnc_id = False
            continue
        if '_multiword_' in matched_token:

                #   We extract placeholder
                #   e.g: ['Lexeme', ' _multiword_1 -> Classification', ' Arithmetic Operation']
            placeholder = matched_token.split("`")[1].strip() 

                # Get placeholder (_multiword_1)
            placeholder = placeholder.split()[0]

            if placeholder in placeholders: 
                orig_phrase = placeholders[placeholder]

                # Match original phrase and classify 
                for pattern, category in regex_patterns.items(): # loop through all regexes
                    if re.fullmatch(pattern, orig_phrase): # check if there is a match between the regex and the original phrase
                        if category == "Function Call" or category == "Function Statement":
                            next_token_is_fnc_id = True
                        elif category == "Loop Delimeter":
                            next_token_is_loop_id = True
                        final_tokens.append(f"Lexeme` {orig_phrase} -> Classification ` {category}")
                        break
            else: 
                final_tokens.append(matched_token)
        else:
            final_tokens.append(matched_token)
    
    line_lexemes = []
    line_classifications = []
    for final_token in final_tokens:
        # Split the token into lexeme and classification
        # Note: In case you want to see, or get the strings (e.g: Lexeme: NOOB -> Classification: Lmao), you can access these using final_token
        parts = final_token.split(" -> ")
        lexeme = parts[0].split("`")[1].strip()
        classification = parts[1].split("`")[1].strip()
        line_lexemes.append(lexeme)
        line_classifications.append(classification)
    line_lexemes.append("\n")
    line_classifications.append("Linebreak")
            
    return line_lexemes, line_classifications
# Function to read the file and process each line
def get_lexemes(tokenizedList):

        # Instantiate the lexemes and classifications arrays (contains all lexemes and classifications of the input file)
    lexemes = []
    classifications = []
        # Flag to indicate if the line is part of multiline comment
    multiline_comment = False
    for element in tokenizedList:
                # While multiline comment is true, and tldr not found, ignore line
            if multiline_comment and element.strip() != "TLDR": 
                continue
            else:
                multiline_comment = False
            line = element.strip()
            if line:
                print(f"\nProcessing line: {line}")
                
                # If OBTW is detected set flag to true
                if(line.strip() == "OBTW"): 
                    multiline_comment = True
                line_lexeme, line_classification = tokenize_and_match(line)
                lexemes.extend(line_lexeme)
                classifications.extend(line_classification)



    return list(zip(lexemes, classifications))