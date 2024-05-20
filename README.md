Web Scraper for Laptop Prices in Syria And in the Amazon shop

This is an explanation of my application that retrieves data from specific websites. I want to include it as a description for the project.

The code above collects product information from two websites, Amazon and Laptop.sy, using Python.

It starts by defining the Product object, which represents a product. The object has the following properties:

    name: the name of the product
    price: the price of the product
    description: the description of the product
    specifications: the technical specifications of the product
    rating: the rating of the product

The amazon() function then collects the product information from the Amazon website. It starts by opening a web browser using Selenium and loading the search results page for laptops. It then extracts the data using BeautifulSoup.

For each laptop on the page, it extracts the name, price, rating, and link. It then opens the product page and extracts the description and technical specifications. The information is stored in a Product object and added to the list of products.

This is followed by the laptopsy() function, which collects the product information from the Laptop.sy website. It uses the requests and BeautifulSoup libraries to perform a similar process, with some differences in the page structure and data extraction method.

Both functions add the collected information to the products list.

Finally, the save_products() function saves the collected information to a CSV or JSON file. It defines the field names and uses the csv and json libraries to write the data to the respective files.

The main main() function runs the amazon() and laptopsy() functions and calls save_products() to save the data in CSV and JSON files.
