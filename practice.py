'''
Authors:
Klenn Jakek Borja
Shawn Clyde Diares
Kervin Ralph Samson

Section: ST1L
'''
import re
from tkinter import Tk, filedialog

# Define regex patterns for specific keywords/phrases

regex_patterns = {
    r'^HAI$': 'Code Delimeter',
    r'^KTHXBYE$': 'Code Delimeter',
    r'^I HAS A$': 'Variable Declaration',  # This will match the full phrase "I HAS A"
    r'^WAZZUP$' : 'Declare Variables',
    r'^BUHBYE$' : 'Declare Variables',
    r'^BTW$' : 'Single Line Comment',
    r'^OBTW$' : 'Multiple Line Comment',
    r'^TLDR$' : 'Multiple Line Comment',
    r'^ITZ$' : 'Variable Assignment',
    r'^R$' : 'Variable Assignment',
    r'^SUM OF$' : 'Arithmetic Operation',
    r'^DIFF OF$' : 'Arithmetic Operation',
    r'^PRODUKT OF$' : 'Arithmetic Operation',
    r'^QUOSHUNT OF$' : 'Arithmetic Operation',
    r'^MOD OF$' : 'Arithmetic Operation',
    r'^BIGGR OF$' : 'Comparison Operation',
    r'^SMALLR OF$' : 'Comparison Operation',
    r'^BOTH OF$' : 'Boolean Operation',
    r'^EITHER OF$' : 'Boolean Operation',
    r'^WON OF$' : 'Boolean Operation',
    r'^NOT$' : 'Boolean Operation',
    r'^ANY OF$' : 'Boolean Operation',
    r'^ALL OF$' : 'Boolean Operation',
    r'^BOTH SAEM$' : 'Comparison Operation',
    r'^DIFFRINT$' : 'Comparison Operation',
    r'^SMOOSH$' : 'String Operation',
    r'^MAEK$' : 'Typecasting',
    r'^AN$' : 'ASK MAAM/UNKNOWN',
    r'^IS NOW A$' : 'Typecasting',
    r'^VISIBLE$' : 'Output Keyword',
    r'^O RLY\?$' : 'Conditional Statement',
    r'^YA RLY$' : 'Conditional Statement',
    r'^MEBBE$' : 'Conditional Statement',
    r'^NO WAI$' : 'Conditional Statement',
    r'^OIC$' : 'Conditional Statement',
    r'^WTF\?$' : 'Case Statement',
    r'^OMG$' : 'Case Statement',
    r'^OMGWTF$' : 'Case Statement',
    r'^IM IN YR$' : 'Loop Statement',
    r'^UPPIN$' : 'Loop Statement',
    r'^NERFIN$' : 'Loop Statement',
    r'^YR$' : 'Loop Statement',
    r'^TIL$' : 'Loop Statement',
    r'^IM OUTTA YR$' : 'Loop Statement',
    r'^HOW IZ I$' : 'Function Statement',
    r'^IF U SAY SO$' : 'Function Statement',
    r'^GTFO$' : 'Break/Return',
    r'^FOUND YR$' : 'Return',
    r'^I IZ$' : 'Function Call',
    r'^MKAY$' : 'Arity Delimiter',
    r'\"': 'String Delimiter',
    # Identifier regex pattern, make sure this comes after specific cases like delimiters
    r'^(-?[1-9][0-9]*|0)$' : 'Literal',
    r'^-?\d*\.\d+$' : 'Literal',  # Fixed pattern for floating-point literals
    r'"[^"]*"|[^"\s]+' : 'Literal', # this was changed
    r'^(WIN|FAIL)$' : 'Literal',
    r'^(NOOB|NUMBA?R|YARN|TROOF)$' : 'Literal',
    r'^([a-zA-Z][a-zA-Z0-9_]*)$': 'Variable Identifier',
    r'^([a-zA-Z][a-zA-Z0-9_]*\(.*\))$' : 'Function Identifier',
    r'^([a-zA-Z][a-zA-Z0-9_]*\(.*\))$' : 'Loop Identifier'
}

# Function to tokenize and match each token
def tokenize_and_match(line):

    # Step 1: Handle quoted strings and preserve them as one token
    # This will match any quoted string and preserve it as a single token
    quoted_string_pattern = r'"[^"]*"|[^"\s]+'
    tokens = []
    
    # contains the multiword regexes (highest priority in checking)
    multiword_regexes = [regex[1:-1] for regex in regex_patterns.keys() if len(regex.split()) > 1]

    # We match the string based on its priority list
    # Find all quoted strings and add them to the tokens list
    # Step 2.1: Find all multiword strings and add them to the tokens list

    placeholders = {}
    placeholder_counter = 1

    for regex in multiword_regexes:

        for match in re.finditer(regex, line):
            
            placeholder = f"_multiword_{placeholder_counter}"
            line = line.replace(match.group(0), placeholder, 1)
            # add placeholder to dictionary
            placeholders[placeholder] = match.group(0)
            placeholder_counter += 1

    # # Step 2.2: Split the remaining line by spaces, ensuring no quoted strings are split
    for match in re.finditer(quoted_string_pattern, line):
        if(match.group(0).startswith('"') and match.group(0).endswith('"')):
            tokens.append("\"")
            tokens.append(match.group(0))
            tokens.append("\"")
            continue
        if(match.group(0) == "BTW" or match.group(0) == "OBTW" or match.group(0) == "TLDR"):
            tokens.append(match.group(0))
            break
        tokens.append(match.group(0))
    

    # Step 3: Match each token with the regex patterns
    # matched_tokens contain the substituted multiwords
    matched_tokens = []

    # this for loop iterates over each token with a quotation mark which indicates a string literal
    for token in tokens:
        # bool flag to check if a match is found
        matched = False
        for pattern, category in regex_patterns.items(): # pattern = key , category = value
            if re.fullmatch(pattern, token): # dapat exact 

                # if category is a string literal, then we remove its quotes and print
                if category == "Literal" and token.startswith('"') and token.endswith('"'):
                    x = slice(1,-1)

                    matched_tokens.append(f"Lexeme: {token[x]} -> Classification: {category}")
                    matched = True
                    break

                # if it is not a string literal, it immediately appends
                matched_tokens.append(f"Lexeme: {token} -> Classification: {category}")
                matched = True
                break  # Stop checking once a match is found

        if not matched:
            matched_tokens.append(f"No match for: {token}")

    # replace the multiwords with its original names (which is indicated by the placeholders dictionary)
    # this indicates that the statement after a function category is a function identifier
    next_token_is_fnc_id = False
    final_tokens = []

    for matched_token in matched_tokens:
        if next_token_is_fnc_id:
            final_tokens.append(f"Lexeme: {matched_token.split(":")[1].strip()} : Function Identifier")
            next_token_is_fnc_id = False
            continue
        if '_multiword_' in matched_token:
            # extract placeholder
            placeholder = matched_token.split(":")[1].strip() # ['Lexeme', ' _multiword_1 -> Classification', ' Arithmetic Operation']
            placeholder = placeholder.split()[0] # get placeholder (_multiword_1)

            if placeholder in placeholders: # check if inside then assign it to orig_phrase
                orig_phrase = placeholders[placeholder]

                # match original phrase and classify 
                for pattern, category in regex_patterns.items(): # loop through all regexes
                    if re.fullmatch(pattern, orig_phrase): # check if there is a match between the regex and the original phrase
                        if category == "Function Call" or category == "Function Statement":
                            next_token_is_fnc_id = True
                        final_tokens.append(f"Lexeme: {orig_phrase} -> Classification : {category}")
                        break
            else: # if placeholder was not found
                final_tokens.append(matched_token)
        # if _multiword_ is not found
        else:
            final_tokens.append(matched_token)
            


    # print final matched tokens 
    for final_token in final_tokens:
        print(final_token)

# Function to read the file and process each line
def process_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                print(f"\nProcessing line: {line}")
                tokenize_and_match(line)

def main():
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(filetypes=[("LOL Files", "*.lol")])
    if file_path:
        process_file(file_path)

main()