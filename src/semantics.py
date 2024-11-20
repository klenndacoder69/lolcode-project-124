import re

# Function for checking if a value is float
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
# This function returns the result of an arithmetic operation
def arithmetic_operation(line, variable_storage):
    """
    Evaluates arithmetic expressions in LOLCODE, handling nested operations and variables.

    Args:
        line (str): The arithmetic expression (e.g., "SUM OF 5 AN 4").
        variable_storage (dict): Dictionary storing variable values.

    Returns:
        The result of the arithmetic operation.
    """
    
    # Remove leading and trailing whitespaces
    line = line.strip()

    # Identify the operation and extract operands
    if line.startswith("SUM OF"):
        operands = line[7:].strip().split(" AN ")
        result = sum(map(lambda x: evaluate_operand(x, variable_storage), operands))
    elif line.startswith("DIFF OF"):
        operands = line[8:].strip().split(" AN ")
        result = evaluate_operand(operands[0], variable_storage) - evaluate_operand(operands[1], variable_storage)
    elif line.startswith("PRODUKT OF"):
        operands = line[11:].strip().split(" AN ")
        result = 1
        for operand in operands:
            result *= evaluate_operand(operand, variable_storage)
    elif line.startswith("QUOSHUNT OF"):
        operands = line[11:].strip().split(" AN ")
        result = evaluate_operand(operands[0], variable_storage) / evaluate_operand(operands[1], variable_storage)
    elif line.startswith("MOD OF"):
        operands = line[7:].strip().split(" AN ")
        result = evaluate_operand(operands[0], variable_storage) % evaluate_operand(operands[1], variable_storage)
    else:
        raise ValueError(f"Unsupported operation: {line}")

    return result

def evaluate_operand(operand, variable_storage):
    """
    Evaluates an operand, which can be a number or a variable.
    
    Args:
        operand (str): The operand to evaluate (could be a number or a variable).
        variable_storage (dict): Dictionary storing variable values.

    Returns:
        The evaluated value of the operand (int or float).
    """
    
    # Check if the operand is a number (float or integer)
    if operand.isdigit() or isfloat(operand):
        return float(operand) if isfloat(operand) else int(operand)
    
    # If the operand is a variable, retrieve its value from the variable storage
    if operand in variable_storage:
        return variable_storage[operand]
    
    # If the operand is a variable but doesn't exist in storage, raise an error
    raise ValueError(f"Variable '{operand}' is not initialized.")

def variable_declaration(line, variable_storage):
    """
    Process a variable declaration line in LOLCODE and store the variable in `variable_storage`.

    Args:
        line (str): The line containing the variable declaration.
        variable_storage (dict): Dictionary to store variable names and their values/types.
    """
    parts = line.strip().split(" ITZ ")
    variable_name = parts[0].strip()

    if len(parts) == 1:
        # Uninitialized variable
        variable_storage[variable_name] = None
    else:
        # Initialized variable
        value = parts[1].strip()

        # Handle different types of initializations
        if value.startswith('"') and value.endswith('"'):
            # Literal (string)
            variable_storage[variable_name] = value.strip('"')
        elif re.match(r'^-?\d+(\.\d+)?$', value):
            # Literal (integer or float)
            variable_storage[variable_name] = float(value) if '.' in value else int(value)
        elif value.isidentifier():
            # Variable reference
            if value in variable_storage:
                variable_storage[variable_name] = variable_storage[value]
            else:
                raise ValueError(f"Variable '{value}' used before initialization.")
        elif any(op in value for op in ["SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF"]):
            # Arithmetic expression
            try:
                variable_storage[variable_name] = arithmetic_operation(value, variable_storage)
            except ValueError as e:
                raise ValueError(f"Invalid arithmetic expression in line: {line}. Error: {str(e)}")
        else:
            raise ValueError(f"Unsupported initialization format: {value}")

def get_semantics(file_content):
    """
    Parse LOLCODE semantics and analyze the file content.

    Args:
        file_content (list of str): Lines of LOLCODE source code.
    """
    variable_storage = {}
    classifications = [
        'Code Delimeter', 'Variable Declaration', 'Declare Variables', 'Single Line Comment',
        'Multiple Line Comment', 'Variable Assignment', 'Operator', 'Arithmetic Operation',
        'Comparison Operation', 'Boolean Operation', 'String Operation', 'Typecasting',
        'ASK MAAM/UNKNOWN', 'Output Keyword', 'Input Keyword', 'Conditional Statement',
        'Case Statement', 'Loop Delimiter', 'Loop Statement', 'Function Statement',
        'Function Call', 'Arity Delimiter', 'Break/Return', 'Return', 'Literal', 'Variable Identifier',
        'Function Identifier', 'Loop Identifier'
    ]

    declare_flag = False

    for line in file_content:
        # Ignore HAI and KTHXBYE
        if line.strip() == "HAI":
            continue
        if line.strip() == "KTHXBYE":
            break
        if line.strip() == "WAZZUP":
            declare_flag = True
            continue
        if line.strip() == "BUHBYE":
            declare_flag = False
            continue
        # Handle variable declaration
        if line.strip().startswith("I HAS A") and declare_flag == True:
            try:
                variable_declaration(line.split("I HAS A", 1)[1], variable_storage)
            except ValueError as e:
                print(f"Error processing line: {line.strip()} - {e}")

        # You can expand this section for handling other classifications

    print("Variable Storage:", variable_storage)
