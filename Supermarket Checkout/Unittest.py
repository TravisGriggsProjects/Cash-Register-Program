import unittest
from unittest.mock import mock_open, patch
from CheckoutRegister import CheckoutRegister
from Product import Product  # Assuming Product is in another file

class TestCheckoutRegister(unittest.TestCase):

    def setUp(self):
        """Initialize the test setup."""
        # Create an instance of the CheckoutRegister and a sample product
        self.register = CheckoutRegister()
        self.product = Product("12345", "Test Product", 5.99)  # Barcode, name, price

    @patch("builtins.open", new_callable=mock_open, read_data="12345,Test Product,5.99\n")
    def test_scan_item_valid(self, mock_file):
        """Test scanning a valid item."""
        scanned_product = self.register.scan_item("12345")
        self.assertIsNotNone(scanned_product)  # Ensure a product is returned
        self.assertEqual(scanned_product.get_name(), "Test Product")
        self.assertEqual(self.register.get_amount_due(), 5.99)

    def test_scan_item_invalid(self):
        """Test scanning an invalid item (not in the register)."""
        scanned_product = self.register.scan_item("00000")
        self.assertIsNone(scanned_product)  # Expect None for an invalid product

    def test_accept_payment(self):
        """Test the accept_payment method."""
        self.register.set_amount_due(10.00)
        self.register.accept_payment(7.00)
        self.assertEqual(self.register.get_amount_received(), 7.00)
        self.assertEqual(self.register.get_amount_due() - self.register.get_amount_received(), 3.00)

    def test_init(self):
        """Test initialization of the CheckoutRegister."""
        self.assertEqual(self.register.get_amount_due(), 0)
        self.assertEqual(self.register.get_amount_received(), 0)
        self.assertEqual(self.register.get_items(), [])


class TestProduct(unittest.TestCase):

    def setUp(self):
        """Initialize a sample product."""
        self.product = Product("12345", "Test Product", 5.99)

    def test_get_barcode(self):
        """Test the get_barcode method."""
        self.assertEqual(self.product.get_barcode(), "12345")

    def test_get_name(self):
        """Test the get_name method."""
        self.assertEqual(self.product.get_name(), "Test Product")

    def test_get_price(self):
        """Test the get_price method."""
        self.assertEqual(self.product.get_price(), 5.99)

if __name__ == '__main__':
    unittest.main()
