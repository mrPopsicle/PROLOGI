import re
functions = ['sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'log', 'ln', 'exp']

def tokenize(expr):
    functions_local = functions
    tokens = []
    i = 0
    while i < len(expr):
        char = expr[i]

        if char in ' \t\n':
            i += 1
            continue

        if char in '+-*/^()':
            # Handle negative numbers
            if char == '-' and (i == 0 or expr[i-1] in '+-*/^('):
                num = '-'
                i += 1
                while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                    num += expr[i]
                    i += 1
                if num == '-':  # Just a minus operator
                    tokens.append(char)
                else:
                    tokens.append(float(num) if '.' in num else int(num))
                continue
            else:
                tokens.append(char)
                i += 1
            continue

        # Numbers
        if char.isdigit() or char == '.':
            num = char
            i += 1
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                num += expr[i]
                i += 1
            tokens.append(float(num) if '.' in num else int(num))
            continue

        # Check for function names first
        matched = False
        for function in functions_local:
            if expr[i:i+len(function)] == function:
                tokens.append(function)
                i += len(function)
                matched = True
                break
        if matched:
            continue

        # Otherwise, treat as variable (single letter like x, y)
        if char.isalpha():
            tokens.append(char)
            i += 1
            continue

        raise ValueError(f"Unknown character: '{char}'")

    # Add implied multiplication
    new_tokens = []
    for i in range(len(tokens)):
        current = tokens[i]
        new_tokens.append(current)

        if i + 1 < len(tokens):
            nxt = tokens[i + 1]
            # Cases where we need implied multiplication:
            # 1) number followed by variable or function or '('
            # 2) variable followed by number or variable or function or '('
            # 3) ')' followed by number or variable or function or '('
            if ((isinstance(current, (int, float)) and (isinstance(nxt, str) and nxt not in '+-*/^()')) or
                (current == ')' and (isinstance(nxt, (int, float)) or (isinstance(nxt, str) and nxt not in '+-*/^()'))) or
                (isinstance(current, str) and current not in '+-*/^()' and 
                 isinstance(nxt, str) and nxt not in '+-*/^()' and not (current in functions or nxt in functions))):
                new_tokens.append('*')

    return new_tokens

def differentiate(tokens):
    
    def diff_term(term):
        if isinstance(term, (int, float)):
            return 0
        elif term == 'x':
            return 1
        elif isinstance(term, str):  # other variables
            return 0
        return term 
    if len(tokens) == 1:
        return [diff_term(tokens[0])]  # e.g., [-3] → [0], ['x'] → [1]
    if tokens[1] == '*':
        u, v = tokens[0], tokens[2]
        du, dv = differentiate([u]), differentiate([v])
        # Simplify cases where one derivative is 0
        if du == [0]:
            return dv if u == 1 else [u, '*'] + dv  
        elif dv == [0]:
            return du if v == 1 else du + ['*', v]
        else:
            return du + ['*', v, '+', u, '*'] + dv

    def diff_function(func, arg_tokens):
        # For trig, and logarithmic
        if func == 'sin':
            outer_diff = ['cos', '('] + arg_tokens + [')']
        elif func == 'cos':
            outer_diff = ['-', 'sin', '('] + arg_tokens + [')']
        elif func == 'tan':
            outer_diff = ['sec', '('] + arg_tokens + [')', '^', '2']
        elif func == 'cot':
            outer_diff = ['-', 'csc', '('] + arg_tokens + [')', '^', '2']
        elif func == 'sec':
            outer_diff = ['sec', '('] + arg_tokens + [')', '*', 'tan', '('] + arg_tokens + [')']
        elif func == 'csc':
            outer_diff = ['-', 'csc', '('] + arg_tokens + [')', '*', 'cot', '('] + arg_tokens + [')']
        elif func == 'log':
            outer_diff = ['1', '/', 'x']
        elif func == 'ln':
            inner_diff = differentiate(arg_tokens)
            one_over_u = ['(', '1', '/', '('] + arg_tokens + [')', ')']
            return inner_diff + ['*'] + one_over_u
        elif func == 'exp':
            outer_diff = ['exp', '('] + arg_tokens + [')']
        else:
            return [func] + ['('] + arg_tokens + [')']

        # Then multiply by the derivative of the inner function (chain rule)
        inner_diff = differentiate(arg_tokens)
        if inner_diff == 0:
            return 0
        elif inner_diff == 1:  # Skip multiplying by 1
            return outer_diff
        else:
            return outer_diff + ['*'] + [inner_diff] 
        
    if not tokens:
        return []

    # Handle basic cases
    if len(tokens) == 1:
        return [diff_term(tokens[0])]

    # Handle function calls
    if tokens[0] in ['sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'log', 'ln', 'exp'] and tokens[1] == '(':
        # Find matching parenthesis
        paren_count = 1
        end = 2
        while end < len(tokens) and paren_count > 0:
            if tokens[end] == '(':
                paren_count += 1
            elif tokens[end] == ')':
                paren_count -= 1
            end += 1
        arg_tokens = tokens[2:end-1]
        return diff_function(tokens[0], arg_tokens)

    # Handle addition/subtraction
    if tokens[1] in '+-':
        left = differentiate(tokens[:1])
        right = differentiate(tokens[2:])
        return left + [tokens[1]] + right

    # Handle multiplication (product rule)
    if tokens[1] == '*':
        left = tokens[:1]
        right = tokens[2:]
        left_diff = differentiate(left)
        right_diff = differentiate(right)
        # Product rule: (uv)' = u'v + uv'
        term1 = left_diff + ['*'] + right
        term2 = left + ['*'] + right_diff
        return term1 + ['+'] + term2

    # Handle division (quotient rule)
    if tokens[1] == '/':
        numerator = tokens[:1]
        denominator = tokens[2:]
        num_diff = differentiate(numerator)
        denom_diff = differentiate(denominator)
        # Quotient rule: (u/v)' = (u'v - uv')/v^2
        term1 = num_diff + ['*'] + denominator
        term2 = numerator + ['*'] + denom_diff
        numerator_diff = term1 + ['-'] + term2
        denominator_diff = denominator + ['^', 2]
        return ['('] + numerator_diff + [')', '/', '('] + denominator_diff + [')']

    # Handle exponentiation
    if tokens[1] == '^':
        base = tokens[:1]
        exponent = tokens[2:]
        if isinstance(exponent[0], (int, float)):  # Power rule
            new_exponent = exponent[0] - 1
            coeff = exponent[0]
            return [coeff, '*'] + base + ['^', new_exponent, '*'] + differentiate(base)
        else:  # Exponential rule (a^f(x))
            return ['ln'] + base + ['*'] + tokens + ['*'] + differentiate(exponent)

    # Handle parentheses
    if tokens[0] == '(':
        # Find matching parenthesis
        paren_count = 1
        end = 1
        while end < len(tokens) and paren_count > 0:
            if tokens[end] == '(':
                paren_count += 1
            elif tokens[end] == ')':
                paren_count -= 1
            end += 1
        inner_diff = differentiate(tokens[1:end-1])
        return ['('] + inner_diff + [')']

    return [0]  

def to_string(tokens):
    output = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if isinstance(token, list):  # Handle nested lists (e.g., from differentiate)
            output.append(to_string(token))
        elif token == '(':
            output.append('(')
        elif token == ')':
            output.append(')')
        elif isinstance(token, (int, float)):
            output.append(str(token))
        elif token in '+-*/^':
            output.append(f' {token} ')
        else:  # Functions or variables
            output.append(token)
        i += 1
    return ''.join(output).replace(' )', ')').replace('( ', '(')
    
def main_menu():
    while True:
        print("\n==== Derivatives Calculator ====")
        expr = input("Enter a function to differentiate (or type 'exit' to return): ")
        if expr.lower() == 'exit':
            break
        try:
            tokens = tokenize(expr)
            derivative_tokens = differentiate(tokens)
            derivative = to_string(derivative_tokens)
            print("Derivative:", derivative)
        except Exception as e:
            print("Error", e)

# Example usage:
expr = "4x"
tokens = tokenize(expr)
print("Tokens:", tokens)
derivative = differentiate(tokens)
print("Derivative tokens:", derivative)
print("Derivative:", to_string(derivative))
