# new_review_scrapper

# AUTHOR-AK

## OVERVIEW

This code is a web scraper implemented using Flask that scrapes reviews from the Flipkart website based on a user's search query. The reviews are stored in a CSV file with the name of the file being the search query.

The scraper takes in a user's search query, constructs a URL for the query, and then sends a request to the URL to retrieve the HTML content of the page. It then parses the HTML content using the BeautifulSoup library to extract the relevant data.

The relevant data extracted from the HTML includes the customer name, rating, comment heading, and comment. These data are then stored in a CSV file with the name of the file being the search query.

The code is structured as a Flask application with two routes - one for the homepage and one for the review page. The homepage route renders an HTML template, while the review route handles both GET and POST requests.


## CODE WALKTHROUGH

[1] Importing Required Libraries: The necessary libraries such as Flask, render_template, request, jsonify, requests, BeautifulSoup, pymongo, and logging are imported in the code.

[2] Setting up the Flask App: A Flask instance is created and assigned to the variable 'app'.

[3] Setting up the Homepage: The route for the homepage is set up and the function to be executed when the route is accessed using the GET method is defined. The function simply returns the rendered HTML template.

[4] Setting up the Review Page: The route for the review page is set up and the function to be executed when the route is accessed using the POST or GET method is defined. The function first checks if the request method is POST or GET. If it's POST, then the function extracts the search string from the form data, constructs the URL to be scraped by appending the search string to the base Flipkart URL, sends a request to the URL using the urlopen module, and reads the response from the URL.

When the review page route is accessed using the GET method, the function will render the HTML template for the review page. The template can contain any necessary HTML, CSS, or JavaScript code for displaying the search form, the search results, and any other necessary elements.

In the case of the GET method, the function will not extract any data from the form data because there is no form data to extract. Instead, the function will simply render the HTML template and display it to the user.

In summary, the purpose of the GET method is to retrieve a resource from the server, while the purpose of the POST method is to submit data to be processed by the server. In this case, the GET method is used to display the review page template, while the POST method is used to submit a search query and retrieve search results.

[5] Parsing HTML Content: The HTML content of the page is parsed using BeautifulSoup and the relevant product boxes are found by searching for all divs with class "_1AtVbE col-12-12". The first three boxes are removed as they contain ads. The first product box is then selected, and the product link is extracted from it. The full product URL is constructed by appending the link to the Flipkart domain. A request is then sent to the product URL using the requests library, and the response content is encoded to utf-8 format. The HTML content of the product page is parsed using BeautifulSoup and all the comment boxes in the HTML with class "_16PBlm" are found.

[6] Extracting Required Data: The required data such as customer name, rating, comment heading, and comment are extracted from each comment box using try-except blocks. The extracted data is then written to a CSV file.

[7] Logging: The logging module is used to log any errors or exceptions that may occur during the execution of the program. In case any of the data such as name, rating, or comment heading is not found, an info message is logged to the scrapper.log file.

[8] Returning Response: Finally, the function returns the rendered HTML template with the reviews data.

[9] Cross-Origin Resource Sharing (CORS): The code has a commented line for setting up the Cross Origin Resource Sharing (CORS) policy using the CORS decorator. CORS is a mechanism that allows many resources (e.g., fonts, JavaScript, etc.) on a web page to be requested from another domain outside the domain from which the resource originated. It is disabled in this code but can be enabled by uncommenting the relevant line of code.
