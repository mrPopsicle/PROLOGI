def parse_algebraic(expr):
    expr = expr.strip().replace(" ", "")
    terms = expr.split("+")
    results = []

    for term in terms:
        if "^" in term:
            before_exp, exp_str = term.split("^")
            exponent = int(exp_str)
            if before_exp[-1].isalpha():
                var = before_exp[-1]
                coef_str = before_exp[:-1]
                coef = int(coef_str) if coef_str else 1
            else:
                var = "0"
                coef = int(before_exp)
        else:
            exponent = 1
            if term[-1].isalpha():
                var = term[-1]
                coef_str = term[:-1]
                coef = int(coef_str) if coef_str else 1
            else:
                var = "0"
                coef = int(term)

        results.append((coef, var, exponent))
    return results


def integrate(coefficients, variables, exponents):
    integrated_terms = []
    #Using da zip function as this will take on multiple iterables as inputs :>
    for coef, var, exp in zip(coefficients, variables, exponents):
        new_exp = exp + 1 #This will add 1 to the exponent of the variable
        
        new_coef1 = coef / new_exp #This will divide the coefficient by the new exponent
        new_coef = coef #This will keep the original coefficient because if the variable is 0, then the integrating should remain as is lmao
        if var == "0": 
            integrated_terms.append(f"{new_coef}x") #This if statement is necessary para hindi idivide yung coefficient sa resulting exponent ng number
        else:
            integrated_terms.append(f"({new_coef1}){var}^{new_exp}")

    return " + ".join(integrated_terms) + " + C"

def main_antiderivative():
    #Get lang yung user input dito
    print("\n=== Antiderivative Calculator ===")
    user_inp = input("Enter your algebraic expression (e.g., 'x^2 + 2x + 3'): ")
    parsed = parse_algebraic(user_inp)
    #Then irrun yung buong define function based dito sa "parsed"
    coefficients = []
    variables = []
    exponents = []
    #This three lists will be stored as variables
    for term in parsed:
        coef, var, exp = term
        coefficients.append(coef)
        variables.append(var)
        exponents.append(exp)

    integrated_func = integrate(coefficients, variables, exponents)

    print("Coefficients:", coefficients)
    print("Variables:", variables)
    print("Exponents:", exponents)
    print("Integrated Function:", integrated_func)
    input("\nPress Enter to return to the main menu...")
