# Importing Flask for creating the application, render_template for rendering HTML templates, request for handling HTTP requests, jsonify for returning JSON responses
from flask import Flask, render_template, request,jsonify

# Importing the Cross Origin Resource Sharing module
from flask_cors import CORS,cross_origin

# Importing the requests library to send HTTP requests using Python
import requests

# Importing BeautifulSoup from the bs4 library to extract data from HTML and XML files
from bs4 import BeautifulSoup as bs

# Importing the urlopen module from urllib.request library to make a request to the URL
from urllib.request import urlopen as uReq

# Importing the logging module for logging any errors or exceptions that may occur during the execution of the program
import logging

# Importing the PyMongo library to work with MongoDB database
import pymongo

# Setting up the basic logging configuration, with the file name scrapper.log
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

# Creating a Flask instance and assigning it to the variable app
app = Flask(__name__)

# Setting up the Cross Origin Resource Sharing (CORS) policy using the CORS decorator
# CORS(app)

# Setting up the route for the homepage, and defining the function to be executed when the route is accessed using the GET method
@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

# Setting up the route for the review page, and defining the function to be executed when the route is accessed using the POST or GET method
@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        try:
            # Retrieving the search string from the form data and replacing any spaces with an empty string

            searchString = request.form['content'].replace(" ","")

            # Constructing the URL to be scraped by appending the search string to the base Flipkart URL
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString

            # Sending a request to the URL using the urlopen module and storing the response in the variable uClient
            uClient = uReq(flipkart_url)

            # Reading the response from the URL and storing it in the variable flipkartPage 
            flipkartPage = uClient.read()

            # Closing the connection to the URL
            uClient.close()

            # Parsing the HTML content of the page using BeautifulSoup and storing the result in the variable flipkart_html
            flipkart_html = bs(flipkartPage, "html.parser")

            # Finding all the product boxes on the page by searching for all divs with class "_1AtVbE col-12-12"
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})

            # Removing the first 3 boxes as they contain ads
            del bigboxes[0:3]

            # Selecting the first product box, as it is usually the most relevant result
            box = bigboxes[0]

            # Extracting the product link from the first product box, and constructing the full product URL by appending the link to the Flipkart domain
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']

            # Sending a request to the product URL using the requests library and storing the response in the variable prodRes
            prodRes = requests.get(productLink)

            # Encoding the response content to utf-8 format
            prodRes.encoding='utf-8'

            # Parsing the HTML content of the product page using BeautifulSoup and storing the result in the variable prod_html
            prod_html = bs(prodRes.text, "html.parser")

            # Printing the entire HTML content of the response
            print(prod_html)

            # Finding all the comment boxes in the HTML with class "_16PBlm"
            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})

            # Setting the name of the file to be saved as a CSV
            filename = searchString + ".csv"

            # Opening the file in write mode and assigning it to the fw variable
            fw = open(filename, "w")

            # Writing the header row to the CSV file
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)

            # Creating an empty list to store all the reviews
            reviews = []

            # Looping through each comment box and extracting the required data
            for commentbox in commentboxes:

                # Extracting the customer name from the comment box and storing it in the name variable

                try:
                    #name.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text

                except:
                    # Logging an info message if the name is not found
                    logging.info("name")

                try:
                    #rating.encode(encoding='utf-8')

                    # Extracting the rating from the comment box and storing it in the rating variable
                    rating = commentbox.div.div.div.div.text


                except:

                    # If rating is not found, storing "No Rating" in the rating variable and logging an info message
                    rating = 'No Rating'
                    logging.info("rating")

                try:
                    #commentHead.encode(encoding='utf-8')

                    # Extracting the comment heading from the comment box and storing it in the commentHead variable
                    commentHead = commentbox.div.div.div.p.text

                except:

                    # If comment heading is not found, storing "No Comment Heading" in the commentHead variable and logging an info message
                    commentHead = 'No Comment Heading'
                    logging.info(commentHead)

                    # Extracting the customer comment from the comment box and storing it in the custComment variable
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    #custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text
                except Exception as e:

                    # Logging the exception if customer comment is not found
                    logging.info(e)


                # Creating a dictionary to store the extracted data
                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}

                # Appending the dictionary to the reviews list          
                reviews.append(mydict)

            # Logging the final result after all the reviews have been extracted and stored in the reviews list    
            logging.info("log my final result {}".format(reviews))

            # Connecting to the MongoDB database using the pymongo library and inserting the reviews data into the collection "scraper_pwskills_eng"
            client = pymongo.MongoClient("mongodb+srv://pwskills:pwskills@cluster0.ln0bt5m.mongodb.net/?retryWrites=true&w=majority")
            db =client['scrapper_eng_pwskills']
            coll_pw_eng = db['scraper_pwskills_eng']
            coll_pw_eng.insert_many(reviews)
               
            # Returning a rendered HTML template with the reviews data   
            return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            logging.info(e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run(host="0.0.0.0")
