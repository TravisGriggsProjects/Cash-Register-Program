# Travis Griggs Supermarket Checkout: 12/09/2024

import sqlite3
from Product import Product
from SupermarketDAO import SupermarketDAO
from Transaction import Transaction

# Class to represent the checkout register
class CheckoutRegister:
    def __init__(self):
        self.__items = self.load_products_from_db()
        self.__shopping_cart = []  # List of products purchased by the customer
        self.__amount_due = 0
        self.__amount_received = 0
        self.__transactions = []

        # Load products from SQLite
    def load_products_from_db(self):
        conn = sqlite3.connect('supermarket.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Products")
        rows = cursor.fetchall()
        products = []
        for row in rows:
            products.append(Product(row[0], row[1], row[2]))  # barcode, name, price
        conn.close()
        return products

    # Method to save each transaction to a file
    def save_transaction(self, date, barcode, amount):
        transaction = Transaction(date, barcode, amount)
        dao = SupermarketDAO("supermarket.db")
        dao.add_transaction_to_db(transaction)
        dao.close()

    # Method to get the items
    def get_items(self):
        return self.__items

    #Method to get the amount due
    def get_amount_due(self):
        return self.__amount_due

    # Method to set the amount due
    def set_amount_due(self, amount):
        self.__amount_due = amount

    #Method to get the amount received
    def get_amount_received(self):
        return self.__amount_received

    # Method to scan a product by barcode
    def scan_item(self, product_barcode):
        for product in self.__items:
            if product.get_barcode() == product_barcode:
                self.__shopping_cart.append(product)  # Add product to shopping cart
                self.__amount_due += product.get_price()
                return product

        # If the product wasn't found
        print("ERROR!! – scanned barcode is incorrect")
        return None

    # Method to accept a payment from the user
    def accept_payment(self, amount_paid):
        self.__amount_received += amount_paid
        return self.__amount_due - self.__amount_received

    # Method to print a receipt
    def print_receipt(self):
        print("\n----- Final Receipt -----\n")
        for item in self.__shopping_cart:
            print(f"{item.get_name()} - ${item.get_price():.2f}")
        print(f"\nTotal Amount Due: ${self.__amount_due:.2f}")
        print(f"Amount Paid: ${self.__amount_received:.2f}")
        print(f"Change: ${self.__amount_received - self.__amount_due:.2f}\n")

