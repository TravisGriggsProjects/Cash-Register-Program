import pickle
from SupermarketDAO import SupermarketDAO
from Product import Product


def authenticate_user():
    try:
        with open("credentials.dat", "rb") as file:
            credentials = pickle.load(file)
    except FileNotFoundError:
        print("ERROR: Credentials file not found.")
        return False

    username = input("Enter username: ")
    password = input("Enter password: ")

    if credentials.get(username) == password:
        print("Authentication successful!")
        return True
    else:
        print("Authentication failed! Try again.")
        return False


def admin_menu():
    if not authenticate_user():
        return

    dao = SupermarketDAO("supermarket.db")
    while True:
        print("\nAdmin Menu")
        print("1. Add Product to Database")
        print("2. List All Products")
        print("3. Find Product by Barcode")
        print("4. List All Transactions")
        print("5. Display Product Sales Bar Chart")
        print("6. Display Excel Report")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            # Get product barcode with input validation
            while True:
                barcode = input("Enter product barcode: ").strip()
                if not barcode:
                    print("ERROR: Barcode cannot be blank.")
                else:
                    # Check if the barcode already exists
                    if dao.check_product_exists(barcode, None):  # Check only for barcode, name is None
                        print(
                            f"ERROR: Product with barcode '{barcode}' already exists. Please enter a different barcode.")
                    else:
                        break  # Exit the loop if barcode is valid and does not exist

            # Get product name with input validation
            while True:
                name = input("Enter product name: ").strip()
                if not name:
                    print("ERROR: Product name cannot be blank.")
                else:
                    break

            # Get product price with input validation
            while True:
                try:
                    price_input = input("Enter product price: ").strip()
                    if not price_input:
                        print("ERROR: Price cannot be blank.")
                    else:
                        price = float(price_input)
                        if price <= 0:
                            print("ERROR: Price must be a positive number.")
                        else:
                            break
                except ValueError:
                    print("ERROR: Invalid price. Please enter a valid number.")

            # Create Product object
            product = Product(barcode, name, price)

            # Add the product to the database
            if dao.add_product_to_db(product):
                print("Product added successfully.")
            else:
                print("Failed to add product.")

        elif choice == '2':
            products = dao.list_all_products()
            if products:
                for product in products:
                    print(f"{product[0]}: {product[1]} - ${product[2]:.2f}")
            else:
                print("No products found.")

        elif choice == '3':
            while True:
                barcode = input("Enter product barcode: ").strip()  # Strip whitespace to avoid blank input with spaces
                if not barcode:
                    print("ERROR: Barcode cannot be blank. Please try again.")
                else:
                    product = dao.find_product_by_barcode(barcode)
                    if product:
                        # Access product attributes using dot notation
                        print(f"{product.get_barcode()}: {product.get_name()} - ${product.get_price():.2f}")
                    else:
                        print("Product not found.")
                    break


        elif choice == '4':
            transactions = dao.list_all_transactions()
            if transactions:
                for transaction in transactions:
                    print(f"{transaction[1]} - {transaction[2]}: ${transaction[3]:.2f}")
            else:
                print("No transactions found.")

        elif choice == '5':
            dao.display_barchart_of_products_sold()

        elif choice == '6':
            dao.display_excel_report_of_transactions()

        elif choice == '7':
            dao.close()
            print("Exiting...")
            break

        else:
            print("Invalid option. Try again.")
            continue

        # After each operation, ask if the admin wants to do more
        while True:
            more_actions = input("Would you like to perform another action? (Y/N): ").strip().upper()
            if more_actions not in ['Y', 'N']:
                print("ERROR: Invalid input. Please enter 'Y' for Yes or 'N' for No.")
            else:
                break

        if more_actions == 'N':
            dao.close()
            print("Exiting Admin Menu...")
            break


admin_menu()
