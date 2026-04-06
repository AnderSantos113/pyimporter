import re
from .phrase_version import parse_version

def compare_versions(installed, spec):
    '''
    Compares an installed version against a specifier.
    
    Parameters:
    - installed: installed version (string), e.g. "1.2.3"
    - spec: condition, e.g. ">=1.2.0", "==1.2.3"

    Supported operators:
    ==, >=, <=, >, <

    Process:
    1. Separates operator and target version
    2. Converts both versions to tuples
    3. Compares according to the operator
    Raises:
    - ValueError: if the format is invalid or version has no numbers
    '''
    
    # Extracts operator and target version (e.g., ">=", "1.2.3")
    match = re.match(r'(==|>=|<=|>|<)(.+)', spec)
    if not match:
        raise ValueError(f"Formato de versión inválido: {spec}")

    op, v = match.groups()

    # Transform versions into tuples of integers for comparison
    v_tuple = parse_version(v)
    i_tuple = parse_version(installed)

    # Operator validation
    valid_operators = {"==", ">=", "<=", ">", "<"}
    if op not in valid_operators:
        raise ValueError(f"Operador no soportado: '{op}'")

    # Perform comparison based on the operator
    if op == "==":
        return i_tuple == v_tuple
    elif op == ">=":
        return i_tuple >= v_tuple
    elif op == "<=":
        return i_tuple <= v_tuple
    elif op == ">":
        return i_tuple > v_tuple
    elif op == "<":
        return i_tuple < v_tuple
    
  