from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars_scrape

# Flask instance
app = Flask(__name__)

# Database connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars_db")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    Mission_Mars = mongo.db.mars_collection.find_one()

    # Return template and data
    return render_template("index.html", Mission_Mars=Mission_Mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = mission_to_mars_scrape.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_collection.update_one({}, {"$set": mars_data}, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)