# Import the functions we need from flask
from flask import Flask
from flask import render_template 
from flask import jsonify
from flask import request
from config import password, username

# Import the functions we need from SQL Alchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Define the database connection parameters
database_name = 'Minneapolis_Restaurants' # Created in Week 9, Night 1, Exercise 08-Stu_CRUD 
connection_string = f'postgresql://{username}:{password}@localhost:5432/{database_name}'

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # Effectively disables page caching

# Here's where we define the various application routes ...
@app.route("/")
def IndexRoute():
    ''' This function runs when the browser loads the index route. 
        Note that the html file must be located in a folder called templates. '''

    webpage = render_template("index.html")
    return webpage

@app.route("/yelp_data", methods=['GET', 'POST'])
def YelpDataRoute():
    
    engine = create_engine(connection_string)
    base = automap_base()
    base.prepare(engine, reflect=True)

    # Choose the table we wish to use
    table = base.classes.yelpdata

    # Open a session, run the query, and then close the session again
    session = Session(engine)
    results = session.query(table.yelpid, table.yelp_name, table.latitude, table.longitude, table.address, table.rating, table.reviews).all()
    session.close()

    # Create a list of dictionaries, with each dictionary containing one row from the query. 
    yelp_reviews = []
    for table.yelpid, table.yelp_name, table.latitude, table.longitude, table.address, table.rating, table.reviews in results:
        dict = {}
        dict["yelpid"] = table.yelpid
        dict["yelp_name"] = table.yelp_name
        dict["latitude"] = table.latitude
        dict["longitude"] = table.longitude
        dict["address"] = table.address
        dict["rating"] = table.rating
        dict["reviews"] = table.reviews
        yelp_reviews.append(dict)

    # Return the jsonified result. 
    return jsonify(yelp_reviews)
    
@app.route("/yelp", methods=['GET', 'POST'])
def YelpRoute():
     
    webpage = render_template("yelp.html")
    return webpage

@app.route("/google_data", methods=['GET', 'POST'])
def GoogleDataRoute():
    
    engine = create_engine(connection_string)
    base = automap_base()
    base.prepare(engine, reflect=True)

    # Choose the table we wish to use
    table = base.classes.googledata

    # Open a session, run the query, and then close the session again
    session = Session(engine)
    results = session.query(table.googleplacesid, table.google_name, table.latitude, table.longitude, table.address, table.rating, table.reviews).all()
    session.close()

    # Create a list of dictionaries, with each dictionary containing one row from the query. 
    google_reviews = []
    for table.googleplacesid, table.google_name, table.latitude, table.longitude, table.address, table.rating, table.reviews in results:
        dict = {}
        dict["google_id"] = table.googleplacesid
        dict["google_name"] = table.google_name
        dict["latitude"] = table.latitude
        dict["longitude"] = table.longitude
        dict["address"] = table.address
        dict["rating"] = table.rating
        dict["reviews"] = table.reviews
        google_reviews.append(dict)

    # Return the jsonified result. 
    return jsonify(google_reviews)
    
@app.route("/google", methods=['GET', 'POST'])
def GoogleRoute():
     
    webpage = render_template("google.html")
    return webpage

@app.route("/health", methods=['GET', 'POST'])
def HealthRoute():

    webpage = render_template("health.html")
    return webpage

@app.route("/health_data")
def HealthDataRoute():
    
    #need this in order to refresh the page
    engine = create_engine(connection_string)
    base = automap_base()
    base.prepare(engine, reflect=True)
    table = base.classes.cleanedinspectiondata

    # Open a session, run the query, and then close the session again
    session = Session(engine)
    results = session.query(table.businessname, table.dateifinspection, table.fulladdress, table.inspectiontype, table.inspectionscore).all()
    session.close()

    # Create a list of dictionaries, with each dictionary containing one row from the query.
    health_array = []
    for table.businessname, table.dateifinspection, table.fulladdress, table.inspectiontype, table.inspectionscore in results:
        dict = {}
        dict["businessname"] = table.businessname
        dict["dateifinspection"] = table.dateifinspection
        dict["fulladdress"] = table.fulladdress
        dict["inspectiontype"] = table.inspectiontype
        dict["inspectionscore"] = table.inspectionscore
        dict["latitude"] = table.latitude
        dict["longitude"] = table.longitude
        health_array.append(dict)

    # Return the jsonified result.
    return jsonify(health_array)

@app.route("/test")
def TestRoute():
    ''' This function returns a simple message, just to guarantee that
        the Flask server is working. '''

    return "This is the test route!"

# This statement is required for Flask to do its job. 
# Think of it as chocolate cake recipe. 
if __name__ == '__main__':
    app.run(debug=True)