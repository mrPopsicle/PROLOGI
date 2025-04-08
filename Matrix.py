import numpy as np

def get_matrix(name):
    """
    Prompts user to input a matrix.
    """
    rows = int(input(f"Enter number of rows for {name}: "))
    columns = int(input(f"Enter number of columns for {name}: "))
    print(f"Enter the elements of {name} row by row (seprated by space): ")

    matrix = []
    for i in range(rows):  
        row = list(map(float, input(f"Row {i + 1}: ").split()))
        while len(row) != columns:
            print(f"Please enter exactly {columns} values.")
            row = list(map(float, input(f"Row {i + 1}: ").split()))
        matrix.append(row)

    return np.array(matrix)

def add_matrices():
    """
    For adding matrices
    """
    print("\n=== Matrix Addition ===")
    A = get_matrix("Matrix A")
    B = get_matrix("Matrix B")
    if A.shape != B.shape:
        print("Error: Matrices must be the same size for addition.")
    else:    
        print("Result of A + B:")
        print(A + B)
    input("\nPress Enter to return to the main menu...")

def subtract_matrices():
    """
    For subtraction of two matrices.
    """
    print("\n=== Matrix Subtraction ===")
    A = get_matrix("Matrix A")
    B = get_matrix("Matrix B")
    if A.shape != B.shape:
        print("Error: Matrices must be the same size for subtraction.")
    else:
        print("Result of A - B:")
        print(A - B)
    input("\nPress Enter to return to the main menu...")

def multiply_matrices():
    """
    Multiplies 2 matrices. 
    """
    print("\n=== Matrix Multiplication ===")
    A = get_matrix("Matrix A")
    B = get_matrix("Matrix B")
    if A.shape[1] != B.shape[0]:
        print("Error: Number of columns of A must be equal to number of rows of B.")
    else:
        print("Result of A x B:")
        print(np.dot(A, B)) # multiplication using dot product
    input("\nPress Enter to return to the main menu...")

def determinant():
    """
    Calculates the determinant of a matrix.
    """
    print("\n=== Determinant Calculator ===")
    A = get_matrix("Matrix")
    if A.shape[0] != A.shape[1]:
        print("Error: Determinant can only be calculated for square matrcies.")
    else:
        print("\nMatrix:")
        print(A)
        
        det = np.linalg.det(A)
        rounded_det = round(det, 5) # Rounds up to 5 decimal places
        print(f"\nDeterminant of the matrix: {rounded_det}")
    input("\nPress Enter to return to the main menu...")

def inverse_matrix():
    """
    Caculates the inverse of a matrix if possible.
    """
    print("\n=== Inverse Matrix Calculator ===")
    A = get_matrix("Matrix")
    if A.shape[0] != A.shape[1]:
        print("Error: Inverse can only be calculated for square matrices.")
    else:
        det = np.linalg.det(A)
        if det == 0:
            print("Error: This matrix does not have an inverse (determinant is 0).")
        else:
            print("Inverse of the matrix:")
            print(np.linalg.inv(A))
    input("\nPress Enter to return to the main menu...")

def main_matrix():
    """
    Main menu for the matrix calculator
    """
    while True:
        print("\n=============================")
        print("     MATRIX CALCULATOR")
        print("=============================")
        print("1. Addition of Matrices")
        print("2. Subtraction of Matrices")
        print("3. Multiplication of Matrices")
        print("4. Determinant of a Matrix")
        print("5. Inverse of a Matrix")
        print("6. Exit")

        choice = input("Choose an option (1-6): ")
    
        if choice == "1":
            add_matrices()
        elif choice == "2":
            subtract_matrices()
        elif choice == "3":
            multiply_matrices()
        elif choice == "4":
            determinant()
        elif choice == "5":
            inverse_matrix()
        elif choice == "6":
            print("Exiting program... Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a number between 1 and 6.")

if __name__ == "__main__":
    main_matrix()