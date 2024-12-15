import sqlite3
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from Product import Product

class SupermarketDAO:
    def __init__(self, db_name):
        # Save the database name as an instance variable
        self.db_name = db_name
        self.conn = None

    def setup_db(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Create the Products table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Products (
                    barcode TEXT PRIMARY KEY,
                    name TEXT,
                    price REAL
                );
            """)

            # Insert sample products
            products = [
                ('101', 'Coke', 2.50),
                ('102', 'Coke Zero', 2.25),
                ('103', 'Pepsi', 3.00),
                ('104', 'Fanta', 2.75),
                ('105', 'Lemonade', 3.00),
                ('106', 'Sprite', 3.25)
            ]
            cursor.executemany("INSERT OR IGNORE INTO Products (barcode, name, price) VALUES (?, ?, ?)", products)

            # Create the Transactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    barcode TEXT,
                    amount REAL,
                    FOREIGN KEY (barcode) REFERENCES Products(barcode)
                );
            """)

            # Insert sample transactions
            transactions = [
                ('2024-09-12 15:26:53', '101', 2.50),
                ('2024-09-13 12:56:13', '102', 2.25),
                ('2024-09-14 17:36:45', '103', 3.00),
                ('2024-09-18 10:13:39', '104', 2.75),
                ('2024-09-25 11:42:21', '105', 3.00)
            ]
            for transaction in transactions:
                cursor.execute("""
                    SELECT COUNT(*) FROM Transactions WHERE date = ? AND barcode = ? AND amount = ?
                """, transaction)
                exists = cursor.fetchone()[0]
                if not exists:
                    cursor.execute("INSERT INTO Transactions (date, barcode, amount) VALUES (?, ?, ?)", transaction)

            conn.commit()
        except sqlite3.Error as e:
            print(f"ERROR: Failed to set up the database: {e}")
        finally:
            conn.close()

    def check_product_exists(self, barcode, name):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Products WHERE barcode = ? OR name = ?", (barcode, name))
            result = cursor.fetchone()[0]
            return result > 0
        except sqlite3.Error as e:
            print(f"ERROR: Failed to check product existence: {e}")
            return False
        finally:
            conn.close()

    def add_product_to_db(self, product):
        conn = None
        if self.check_product_exists(product.get_barcode(), product.get_name()):
            print(f"ERROR: Product with barcode '{product.get_barcode()}' or name '{product.get_name()}' already exists.")
            return False

        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Products (barcode, name, price) VALUES (?, ?, ?)",
                           (product.get_barcode(), product.get_name(), product.get_price()))
            conn.commit()
            print("Product added successfully.")
            return True
        except sqlite3.Error as e:
            print(f"ERROR: Failed to add product: {e}")
            return False
        finally:
            conn.close()

    def add_transaction_to_db(self, transaction):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Transactions (date, barcode, amount) VALUES (?, ?, ?)",
                           (transaction.get_date(), transaction.get_barcode(), transaction.get_amount()))
            conn.commit()
            print(f"Transaction for barcode '{transaction.get_barcode()}' added successfully.")
        except sqlite3.Error as e:
            print(f"ERROR: Failed to add transaction: {e}")
        finally:
            conn.close()

    def list_all_products(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Products ORDER BY barcode")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"ERROR: Failed to list all products: {e}")
            return []
        finally:
            conn.close()

    def find_product_by_barcode(self, barcode):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Products WHERE barcode = ?", (barcode,))
            row = cursor.fetchone()
            if row:
                # Ensure the Product class is initialized correctly
                return Product(row[0], row[1], row[2])
            print(f"ERROR: Product with barcode '{barcode}' not found.")
            return None
        except sqlite3.Error as e:
            print(f"ERROR: {e}")
        finally:
            if conn:
                conn.close()

    def list_all_transactions(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Transactions ORDER BY date")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"ERROR: Failed to list all transactions: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def display_barchart_of_products_sold(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Dictionary to store product counts
            product_counts = {}
            cursor.execute("SELECT barcode, COUNT(barcode) FROM Transactions GROUP BY barcode")
            for barcode, count in cursor.fetchall():
                product_counts[barcode] = count

            # Populate lists for product names and quantities
            product_names = []
            quantities = []
            for barcode, count in product_counts.items():
                cursor.execute("SELECT name FROM Products WHERE barcode = ?", (barcode,))
                product_name = cursor.fetchone()[0]
                product_names.append(product_name)
                quantities.append(count)

            # Create an Excel workbook and sheet
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Product Sales Chart"

            # Write data to the Excel sheet
            sheet.append(['Product Name', 'Quantity Sold'])
            for name, quantity in zip(product_names, quantities):
                sheet.append([name, quantity])

            # Create a bar chart
            bar_chart = BarChart()
            bar_chart.title = "Product Sales"
            bar_chart.x_axis.title = "Products"
            bar_chart.y_axis.title = "Quantity Sold"
            data = Reference(sheet, min_col=2, min_row=2, max_row=len(product_names) + 1)
            categories = Reference(sheet, min_col=1, min_row=2, max_row=len(product_names) + 1)
            bar_chart.add_data(data, titles_from_data=False)
            bar_chart.set_categories(categories)
            sheet.add_chart(bar_chart, "E5")

            workbook.save('product_sales_chart.xlsx')
            print("Bar chart has been generated: 'product_sales_chart.xlsx'")
        except sqlite3.Error as e:
            print(f"ERROR: Failed to generate bar chart: {e}")
        finally:
            conn.close()

# Display an Excel report of all transactions
    def display_excel_report_of_transactions(self):
        # Connect to the database
        conn = sqlite3.connect('supermarket.db')
        cursor = conn.cursor()

        # Fetch all transactions but exclude the 'id' column
        cursor.execute("SELECT date, barcode, amount FROM Transactions ORDER BY date")
        transactions = cursor.fetchall()

        # Close the connection
        conn.close()

        # Create an Excel workbook and sheet
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Transactions Report"

        # Write the header
        sheet.append(['Date', 'Barcode', 'Quantity'])

        # Write the transaction data to the Excel file
        for transaction in transactions:
            sheet.append(transaction)

        # Save the workbook
        workbook.save('transactions_report.xlsx')
        print("Excel report has been generated: 'transactions_report.xlsx'")

    def close(self):
        if self.conn:
            self.conn.close()  # Close the database connection
            print("Database connection closed.")
        else:
            print("No active database connection to close.")

# Example usage
dao = SupermarketDAO('supermarket.db')
dao.setup_db()

