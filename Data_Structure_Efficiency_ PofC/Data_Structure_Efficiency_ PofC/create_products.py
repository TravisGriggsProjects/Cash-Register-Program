# Import random module
import random

# Define a function to generate random product details
def generate_product_details():
  # Create an empty list to store the product details
  product_details = []
  MAX_NUMBER = 1000000
  # Loop through the number of products
  for i in range(1,MAX_NUMBER):
    # Generate a random product ID between 1 and 100000
    product_id = i
    # Generate a random name with the format PXXX
    name = "P" + str(random.randint(1, MAX_NUMBER))
    # Generate a random description with the format DESC XXX
    description = "DESC " + str(random.randint(1, MAX_NUMBER))
    # Generate a random price between 0 and 10 with two decimal places
    price = round(random.uniform(0, 10), 2)
    # Create a product detail string with the format ID,NAME,DESCRIPTION,PRICE
    product_detail = str(product_id) + "," + name + "," + description + "," + str(price)
    # Append the product detail to the list
    product_details.append(product_detail)
  # Return the list of product details
  return product_details

# Call the function with the number of products as an argument
product_details = generate_product_details()

# Print the product details
file = open("products.txt", "wt")
for product_detail in product_details:
  file.write(product_detail+"\n")
file.write("1000000,P97872,DESC 22715,1.98")
file.close()