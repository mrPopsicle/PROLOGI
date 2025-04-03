import sys

def help_menu():
    help_ascii = """
    ==============================
    |        HELP MENU           |
    ==============================
    """
    print(help_ascii)
    print("- Derivatives Calculator: Computes the derivative of a function (polynomials, trigonometric functions, logarithmic functions.)")
    print("- Antiderivatives Calculator: Computes the antiderivative of a function.")
    print("- Matrix Calculator: Performs matrix operations.")

def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Derivatives Calculator")
        print("2. Antiderivatives Calculator")
        print("3. Matrix Calculator")
        print("4. Help")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            print("Launching Derivatives Calculator...")
            import Ver1
            Ver1.main_menu()
        if choice == '2':
            print("Work in Progress")
        if choice == '3':
            print("Work in Progress")
        if choice == '4':
            help_menu()
        if choice == '5':
            print("Exiting program... Thank you!")
            sys.exit()
            break
        else:
            print("Invalid choice, please select from 1-5")


if __name__=="__main__":
    main_menu()
