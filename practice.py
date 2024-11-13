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
    # Identifier regex pattern, make sure this comes after specific cases like delimiters
    r'^([a-zA-Z][a-zA-Z0-9_]*)$': 'Variable Identifier',
    r'^([a-zA-Z][a-zA-Z0-9_]*\(.*\))$' : 'Function Identifier',
    r'^([a-zA-Z][a-zA-Z0-9_]*\(.*\))$' : 'Loop Identifier',
    r'^(-?[1-9][0-9]*|0)$' : 'Literal',
    r'^-?\d*\.\d+$' : 'Literal',  # Fixed pattern for floating-point literals
    r'^"\s*[^"]*\s*"$' : 'Literal',
    r'^(WIN|FAIL)$' : 'Literal',
    r'^(NOOB|NUMBA?R|YARN|TROOF)$' : 'Literal',
}

# Function to tokenize and match each token
def tokenize_and_match(line):
    # Step 1: Handle quoted strings and preserve them as one token
    # This will match any quoted string and preserve it as a single token
    quoted_string_pattern = r'"[^"]*"'
    tokens = []
    

    # Find all quoted strings and add them to the tokens list
    for match in re.finditer(quoted_string_pattern, line): # returns an object where it match to access need yung capture
        tokens.append(match.group(0)) # similar to capture in rust 0 = full match bali yung buong nasa loob ng quotation
        print("laman",tokens) # yung enclosed lang sa " "
        line = line.replace(match.group(0), '')  # Remove the quoted string from the line 
        print("ito line",line)

    # Step 2: Split the remaining line by spaces, ensuring no quoted strings are split
    line_tokens = line.split()
    tokens.extend(line_tokens)
    print("end",tokens)

    # Debug: Print tokens before processing
    # print(f"Tokens: {tokens}")
    
    # Step 3: Match each token with the regex patterns
    for token in tokens:
        matched = False
        for pattern, category in regex_patterns.items(): # pattern = key , category = value
            if re.fullmatch(pattern, token): # dapat exact 
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
process_file('read.txt')
