import sys
import Ver1

def help_menu():
    help_ascii = """
    ==============================
    |        HELP MENU           |
    ==============================
    """
    print(help_ascii)
    print("- Derivatives Calculator: Computes the derivative of a function (polynomials, trigonometric functions, logarithmic functions).")
    print("- Antiderivatives Calculator: Computes the antiderivative of a function.")
    print("- Matrix Calculator: Performs matrix operations.")

def main_menu():
    while True:
        print("\n===== Main Menu =====")
        print("1. Derivatives Calculator")
        print("2. Antiderivatives Calculator (WIP)")
        print("3. Matrix Calculator (WIP)")
        print("4. Help")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            print("\nLaunching Derivatives Calculator...")
            try:
                Ver1.main_menu()
            except Exception as e:
                print(f"\n Error: {e}")
        elif choice == '2':
            print("\n Antiderivatives Calculator is a Work in Progress.")
        elif choice == '3':
            print("\n Matrix Calculator is a Work in Progress.")
        elif choice == '4':
            help_menu()
        elif choice == '5':
            print("\nExiting program... Thank you!")
            sys.exit()
        else:
            print("\n Invalid choice! Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main_menu()
