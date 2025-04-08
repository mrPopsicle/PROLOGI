import Derivative
import Antiderivative
import Matrix

def help_menu():
    help_ascii = """
    ==============================
    |        HELP MENU           |
    ==============================
    """
    print(help_ascii)
    print("- Derivatives Calculator: Computes the derivative of a function (polynomials, trigonometric functions, logarithmic functions).")
    print("- Antiderivatives Calculator: Computes the antiderivative of a function.")
    print("- Matrix Calculator: Performs matrix operations (addition, subtraction, multiplication, determinant, inverse of a matrix).")

def main_menu():
    print("================ Calcul8 ================")
    print(" A Calculator program for 3 Math topics")
    print("=========================================")
    
    while True:
        print("\n===== Main Menu =====")
        print("1. Derivatives Calculator")
        print("2. Antiderivatives Calculator")
        print("3. Matrix Calculator")
        print("4. Help")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            print("\nLaunching Derivatives Calculator...")
            try:
                Derivative.main()
            except Exception as e:
                print(f"\n Error: {e}")
        elif choice == '2':
            print("\nLaunching Antiderivatives Calculator...")
            try:
                Antiderivative.main_antiderivative()
            except Exception as e:
                print(f"\nError: {e}")
        elif choice == '3':
            print("\nLaunching Matrix Calculator...")
            try:
                Matrix.main_matrix()
            except Exception as e:
                print(f"\nError: {e}")
        elif choice == '4':
            help_menu()
        elif choice == '5':
            print("\nExiting program... Thank you!")
            break
        else:
            print("\n Invalid choice! Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main_menu()
