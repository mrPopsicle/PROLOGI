def calculate_derivative(expression):
    """Calculate the derivative of a simple mathematical expression
    Supports basic polynomial, trigonometric and logarithmic functions
    """
    # Remove the spaces for easy parsing po
    expression = expression.replace(" ", "")
    
    # Check for sum or difference first 
    terms = split_sum_or_difference(expression)
    if len(terms) > 1:
        # If we have multiple terms then take derivative of each term
        derivatives = []
        for term in terms:
            derivatives.append(calculate_derivative(term))
        return " + ".join(derivatives).replace("+ -", "- ")
    
    # Handle quotient rule
    if "/" in expression:
        return handle_quotient(expression)
    
    # Handle product rule
    if "*" in expression:
        return handle_product(expression)
    
    # Handle exponents outside parenthesis (general power rule with chain rule)
    if ")^" in expression:
        try:
            base, exponent = expression.rsplit(")^", 1)
            base += ")"
            exponent = int(exponent)
            inner = base[1:-1]  # Remove outer parenthesis
            inner_derivative = calculate_derivative(inner)
            return f"{exponent}{base}^{exponent-1} * ({inner_derivative})"
        except ValueError:
            pass
    
    # Handle chain rule for trig and log functions
    if expression.startswith("sin"):
        return handle_sin(expression)
    elif expression.startswith("cos"):
        return handle_cos(expression)
    elif expression.startswith("tan"):
        return handle_tan(expression)
    elif expression.startswith("csc"):
        return handle_csc(expression)
    elif expression.startswith("sec"):
        return handle_sec(expression)
    elif expression.startswith("cot"):
        return handle_cot(expression)
    elif expression.startswith("ln"):
        return handle_ln(expression)
    
    # Handle parenthesis
    if expression.startswith("(") and expression.endswith(")"):
        return calculate_derivative(expression[1:-1])
    
    # Handle polynomials
    if "x" in expression:
        return handle_polynomial(expression)
    
    # Handle constants
    try:
        float(expression)
        return "0"  # Derivative of a constant is 0
    except ValueError:
        return f"Cannot differentiate: {expression}"

def split_sum_or_difference(expression):
    """Split an expression into terms separated by + or -"""
    if "+" not in expression and "-" not in expression:
        return [expression]
    
    terms = []
    current_term = ""
    
    # Track parenthesis level to avoid splitting inside parenthesis
    paren_level = 0
    
    for i, char in enumerate(expression):
        if char == "(":
            paren_level += 1
        elif char == ")":
            paren_level -= 1
        
        
        if (char == "+" or char == "-") and paren_level == 0 and i > 0:
            terms.append(current_term)
            if char == "+":
                current_term = ""
            else:
                current_term = "-"
        else:
            current_term += char
    
    # Add the last term
    if current_term:
        terms.append(current_term)
    
    return terms

def handle_polynomial(expression):
    """Calculate derivative of a polynomial term"""
    # Handle simple cases like x, -x
    if expression == "x":
        return "1"
    elif expression == "-x":
        return "-1"
    
    # Check po for exponent here
    if "^" in expression:
        # Split to coefficients , variable and exponents
        if "x^" in expression:
            parts = expression.split("x^")
            coefficient = parts[0]
            if coefficient == "":
                coefficient = "1"
            elif coefficient == "-":
                coefficient = "-1"
            exponent = parts[1]
        else:
            return "Cannot parse this polynomial"
        
        try:
            coef = int(coefficient)
            exp = int(exponent)
            new_coef = coef * exp
            new_exp = exp - 1
            
            if new_exp == 0:
                return str(new_coef)
            elif new_exp == 1:
                return f"{new_coef}x"
            else:
                return f"{new_coef}x^{new_exp}"
        except ValueError:
            return f"Cannot differentiate: {expression}"
    else:
        # Handle case of coefficient * x (like 5x)
        coef = expression.replace("x", "")
        if coef == "":
            return "1"
        elif coef == "-":
            return "-1"
        else:
            try:
                return coef
            except ValueError:
                return f"Cannot differentiate: {expression}"

def handle_sin(expression):
    """Calculate derivative of sin function"""
    # Extract po from inside sin
    inner = expression[4:-1]  # Remove 'sin(' and ')'
    
    if inner == "x":
        return "cos(x)"
    else:
        # Chain rule
        inner_derivative = calculate_derivative(inner)
        return f"cos({inner}) * ({inner_derivative})"

def handle_cos(expression):
    """Calculate derivative of cos function"""
    # Extract po from inside cos 
    inner = expression[4:-1]  
    
    if inner == "x":
        return "-sin(x)"
    else:
        # Chain rule
        inner_derivative = calculate_derivative(inner)
        return f"-sin({inner}) * ({inner_derivative})"

def handle_tan(expression):
    """Calculate derivative of tan function"""
    # Extract po from inside tan 
    inner = expression[4:-1] 
    
    if inner == "x":
        return "sec^2(x)"
    else:
        # Chain rule
        inner_derivative = calculate_derivative(inner)
        return f"sec^2({inner}) * ({inner_derivative})"

def handle_csc(expression):
    """Calculate derivative of csc function"""
    # Extract po from inside csc
    inner = expression[4:-1]  
    
    if inner == "x":
        return "-csc(x) * cot(x)"
    else:
        # Chain rule
        inner_derivative = calculate_derivative(inner)
        return f"-csc({inner}) * cot({inner}) * ({inner_derivative})"

def handle_sec(expression):
    """Calculate derivative of sec function"""
    # Extract po from inside sec
    inner = expression[4:-1]  
    
    if inner == "x":
        return "sec(x) * tan(x)"
    else:
        # Chain rule
        inner_derivative = calculate_derivative(inner)
        return f"sec({inner}) * tan({inner}) * ({inner_derivative})"

def handle_cot(expression):
    """Calculate derivative of cot function"""
    # Extract po from inside cot
    inner = expression[4:-1]  
    
    if inner == "x":
        return "-csc^2(x)"
    else:
        # Chain rule
        inner_derivative = calculate_derivative(inner)
        return f"-csc^2({inner}) * ({inner_derivative})"

def handle_ln(expression):
    """Calculate derivative of ln function"""
    # Extract po from inside natural log (ln)
    inner = expression[3:-1] 
    
    if inner == "x":
        return "1/x"
    else:
        # Chain rule
        inner_derivative = calculate_derivative(inner)
        return f"({inner_derivative})/({inner})"

def handle_product(expression):
    """Apply product rule: (f*g)' = f'*g + f*g'"""
    # Split by * but respect parenthesis
    factors = []
    current_factor = ""
    parenthesis_level = 0
    
    for char in expression:
        if char == "(":
            parenthesis_level += 1
        elif char == ")":
            parenthesis_level -= 1
        
        if char == "*" and parenthesis_level == 0:
            factors.append(current_factor)
            current_factor = ""
        else:
            current_factor += char
    
    # Add the last factor
    if current_factor:
        factors.append(current_factor)
    
    if len(factors) < 2:
        return "Cannot apply product rule"
    
    f = factors[0]
    g = factors[1]
    
    df = calculate_derivative(f)
    dg = calculate_derivative(g)
    
    return f"({df})*({g}) + ({f})*({dg})"

def handle_quotient(expression):
    """Apply quotient rule: (f/g)' = (f'*g - f*g')/g^2"""
    # Find the numerator and denominator
    parts = expression.split("/")
    if len(parts) != 2:
        return "Cannot parse this fraction"
    
    f = parts[0]
    g = parts[1]
    
    df = calculate_derivative(f)
    dg = calculate_derivative(g)
    
    return f"(({df})*({g}) - ({f})*({dg}))/({g})^2"

def simplify_result(result):
    """Very basic simplification of the result"""
    # Replace +- with -
    result = result.replace("+ -", "- ")
    
    # Remove double negatives
    result = result.replace("--", "")
    result = result.replace(" )", ")")

    # Handle multiplying by 1 or 0
    result = result.replace("* 1", "")
    result = result.replace("1 *", "")
    # Handle if 0 is present
    result = result.replace("+ 0", "")
    
    return result

def main():
    print("\n=================================")
    print("     DERIVATIVE CALCULATOR")
    print("=================================")
    print("Supports: polynomials (x^n)")
    print("trigonometric functions (sin, cos, tan, csc, sec, cot)")
    print("logarithms (ln), products (f*g), and quotients (f/g)")
    
    while True:
        expression = input("\nEnter a mathematical expression (or type 'exit' to end the program): ")
        
        if expression.lower() == 'exit':
            break
        
        try:
            result = calculate_derivative(expression)
            simplified = simplify_result(result)
            print(f"The derivative of {expression} is: {simplified}")
        except Exception as e:
            print(f"Error: {e}")
            print("Please try a simpler expression.")

# # Test cases 
# def test_calculator():
#     test_expressions = [
#         "x^2",
#         "3x^4",
#         "sin(x)",
#         "cos(x)",
#         "tan(x)",
#         "csc(x)",
#         "sec(x)",
#         "cot(x)",
#         "x^2 + 3x + 5",
#         "x * sin(x)",
#         "sin(x^2)",
#         "x/sin(x)",
#         "sec(x^2)"
#     ]
    
#     print("\nTest Results:")
#     for expr in test_expressions:
#         result = calculate_derivative(expr)
#         print(f"d/dx({expr}) = {result}")

if __name__ == "__main__":
    main()
