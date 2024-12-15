# Travis Griggs Supermarket Checkout: 12/09/2024

# Import datetime module to enable representations of date and time.
import datetime

from CheckoutRegister import CheckoutRegister


def main():
    # Loop for each shopper
    while True:

        # Create a new checkout register for each shopper
        register = CheckoutRegister()

        # Loop for scanning items
        while True:

            # Loop to continuously promoted the user to input a barcode until a valid barcode is found
            while True:
                # Ask for the product's barcode
                product_barcode = input("Please enter the barcode of your item: ")
                product = register.scan_item(product_barcode)

                # If the product exists, display its name and price
                if product:
                    print(f"{product.get_name()} - ${product.get_price():.2f}")
                    # Get the current date and time
                    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # Save the transaction details
                    register.save_transaction(date, product.get_barcode(), product.get_price())
                    break

            # Ask if the user wants to scan another item
            while True:
                scan_another_item = input("Would you like to scan another item? (Y/N): ").strip().upper()
                if scan_another_item in ["Y", "N"]:
                    break
                # Handle invalid input
                else:
                    print("ERROR!! – Please enter 'Y' or 'N'.")

            # If the user does not want to scan more items, break the loop
            if scan_another_item == "N":
                break

        # Loop to process payments until the amount due is paid
        while register.get_amount_due() > 0:
            # Display the remaining amount due
            print(f"Payment due: ${register.get_amount_due() - register.get_amount_received():.2f}")

            # Ask for payment amount
            amount_paid = input("Please enter an amount to pay: ")

            try:
                # Convert the input to a float
                amount_paid = float(amount_paid)

                # Check for valid payment
                if amount_paid <= 0:
                    print("ERROR!! – Invalid input. Please enter a positive number.")
                else:
                    # Process the payment and check if the full amount is paid
                    remaining_amount = register.accept_payment(amount_paid)

                    # If payment is complete or overpaid, break the loop
                    if remaining_amount <= 0:
                        break

            # Handle invalid input for payment
            except ValueError:
                print("ERROR!! – Invalid input. Please enter a positive number.")

        # Print the receipt once the payment is done
        register.print_receipt()

        # Ask if there is another shopper
        while True:
            another_shopper = input("Another shopper? (Y/N): ").strip().upper()
            if another_shopper in ["Y", "N"]:
                break

        # If there is another shopper, start the process again
        if another_shopper == "Y":
            print("New Shopper!")

        # If not, exit the program
        elif another_shopper == "N":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
