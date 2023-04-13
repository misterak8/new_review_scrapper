# new_review_scrapper


This code is a web scraper implemented using Flask that scrapes reviews from the Flipkart website based on a user's search query. The reviews are stored in a CSV file with the name of the file being the search query.

The scraper takes in a user's search query, constructs a URL for the query, and then sends a request to the URL to retrieve the HTML content of the page. It then parses the HTML content using the BeautifulSoup library to extract the relevant data.

The relevant data extracted from the HTML includes the customer name, rating, comment heading, and comment. These data are then stored in a CSV file with the name of the file being the search query.

The code is structured as a Flask application with two routes - one for the homepage and one for the review page. The homepage route renders an HTML template, while the review route handles both GET and POST requests.
