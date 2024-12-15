class Transaction:
    def __init__(self, date, barcode, amount):
        self.__date = date
        self.__barcode = barcode
        self.__amount = amount

    def get_date(self):
        return self.__date

    def get_barcode(self):
        return self.__barcode

    def get_amount(self):
        return self.__amount