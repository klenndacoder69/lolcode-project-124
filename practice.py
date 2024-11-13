'''
Authors:
Klenn Jakek Borja
Shawn Clyde Diares
Kervin Ralph Samson

Section: ST1L
'''


import re
# Define regex patterns for specific keywords/phrases
regex_patterns = {
    r'^HAI$': 'Code Delimeter',
    r'^KTHXBYE$': 'Code Delimeter',
    r'^I HAS A$': 'Variable Declaration',  # This will match the full phrase "I HAS A"
    r'^WAZZUP$' : 'Declare Variables',
    r'^BUHBYE$' : 'Declare Variables',
    r'^BTW$' : 'Comment',
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
    r'^VISIBLE$' : 'Output Keyword',
    r'\"': 'String Delimiter',
    # Identifier regex pattern, make sure this comes after specific cases like delimiters
    r'^([a-zA-Z][a-zA-Z0-9_]*)$': 'Variable Identifier',
    r'^([a-zA-Z][a-zA-Z0-9_]*\(.*\))$' : 'Function Identifier',
    r'^([a-zA-Z][a-zA-Z0-9_]*\(.*\))$' : 'Loop Identifier',
    r'^(-?[1-9][0-9]*|0)$' : 'Literal',
    r'^-?\d*\.\d+$' : 'Literal',  # Fixed pattern for floating-point literals
    r'"[^"]*"|[^"\s]+' : 'Literal', # this was changed
    r'^(WIN|FAIL)$' : 'Literal',
    r'^(NOOB|NUMBA?R|YARN|TROOF)$' : 'Literal',
}

# Function to tokenize and match each token
def tokenize_and_match(line):
    # Step 1: Handle quoted strings and preserve them as one token
    # This will match any quoted string and preserve it as a single token
    quoted_string_pattern = r'"[^"]*"|#[^#]*#|[^"\s]+'
    tokens = []
    
    # contains the multiword regexes (highest priority in checking)
    multiword_regexes = [regex[1:-1] for regex in regex_patterns.keys() if len(regex.split()) > 1]
    print(multiword_regexes)
    # pattern = re.compile(multiword_regexes[0])
    # check = pattern.findall("I HAS A HELLO")
    # print(check)
    
    # We match the string based on its priority list
    # Find all quoted strings and add them to the tokens list
    # Step 2.1: Find all multiword strings and add them to the tokens list
    # we should have a loop that contains:
        # 1. find all multiword strings and add them to token list then remove that part of string
        # 2. check for variable
        # 3.
    # while line:

    for regex in multiword_regexes:
        for match in re.finditer(regex, line):
            # tokens.append(match.group(0))
            line = line.replace(match.group(0), f"#{match.group(0)}#", 1)
            # print("test: ", line)
    # # Step 2.2: Split the remaining line by spaces, ensuring no quoted strings are split
    for match in re.finditer(quoted_string_pattern, line):
        print("debug: ", match.group(0))
        if(match.group(0).startswith('#') and match.group(0).endswith('#')):
            slice_hashtag = slice(1,-1)
            tokens.append(match.group(0)[slice_hashtag])
            continue
        if(match.group(0).startswith('"') and match.group(0).endswith('"')):
            tokens.append("\"")
            tokens.append(match.group(0))
            tokens.append("\"")
            continue
        tokens.append(match.group(0))
    print(tokens)
    # return
    # Step 3: Match each token with the regex patterns
    for token in tokens:
        matched = False
        for pattern, category in regex_patterns.items(): # pattern = key , category = value
            if re.fullmatch(pattern, token): # dapat exact 
                # if category is a string literal, then we remove its quotes and print
                if category == "Literal" and token.startswith('"') and token.endswith('"'):
                    x = slice(1,-1)
                    print(f"Lexeme: {token[x]} -> Classification: {category}")
                    matched = True
                    break

                print(f"Lexeme: {token} -> Classification: {category}")
                matched = True
                break  # Stop checking once a match is found
        if not matched:
            print(f"No match for: {token}")

# Function to read the file and process each line
def process_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # Only process non-empty lines
                print(f"\nProcessing line: {line}")
                tokenize_and_match(line)

# Example usage with the file "read.txt"

def main():
    process_file("read.txt")

main()
