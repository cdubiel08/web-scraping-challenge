from flask import Flask, render_template, redirect
from flask_pymongo import pymongo

# From the separate python file in this directory, we'll import the code that is used to scrape craigslist
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create variable for our connection string
conn = 'mongodb://localhost:27017'

# Pass connection string to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. 
# If the database doesn't already exist, our code will 
# create it automatically as soon as we insert a record.
db = client.mission_to_mars

# identify the collection and drop any existing data for this demonstration
html_dict = db.html_dict

# 
@app.route("/")
def index():
    html_data = list(html_dict.find())
    html_data = html_data[0]
    return render_template("index.html", html_data=html_data)

# This route will trigger the webscraping, but it will then send us back to the index route to render the results
@app.route("/scrape")
def scraper():

    html_dict.drop()
    results_dict = scrape_mars.scrape()
    html_dict.insert_one(results_dict)
    
    # Use Flask's redirect function to send us to a different route once this task has completed.
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
