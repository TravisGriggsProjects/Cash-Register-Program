# Travis Griggs Supermarket Checkout: 12/09/2024

# Class to represent individual products
class Product:
    def __init__(self, barcode, name, price):
        self.__barcode = barcode
        self.__name = name
        self.__price = price

    def get_barcode(self):
        return self.__barcode

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price
