# Import the functions we need from flask
from flask import Flask
from flask import render_template 
from flask import jsonify

# Import the functions we need from SQL Alchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Define the database connection parameters
username = 'postgres'  # Ideally this would come from config.py (or similar)
password = 'password'  # Ideally this would come from config.py (or similar)
database_name = 'Minneapolis_Restaurants' # Created in Week 9, Night 1, Exercise 08-Stu_CRUD 
connection_string = f'postgresql://{username}:{password}@localhost:5432/{database_name}'

# Connect to the database
engine = create_engine(connection_string)
base = automap_base()
base.prepare(engine, reflect=True)

# Choose the table we wish to use
table = base.classes.yelpdata
print("table: ", table)

# Instantiate the Flask application. (Chocolate cake recipe.)
# This statement is required for Flask to do its job. 
app = Flask(__name__)

# Here's where we define the various application routes ...
@app.route("/")
def IndexRoute():
    ''' This function runs when the browser loads the index route. 
        Note that the html file must be located in a folder called templates. '''

    webpage = render_template("index.html")
    return webpage

@app.route("/yelp")
def OtherRoute():
    ''' This function runs when the user clicks the link for the other page.
        Note that the html file must be located in a folder called templates. '''

    # Note that this call to render template passes in the title parameter. 
    # That title parameter is a 'Shirley' variable that could be called anything 
    # we want. But, since we're using it to specify the page title, we call it 
    # what we do. The name has to match the parameter used in other.html. 
    webpage = render_template("other.html", title_we_want="Shirley")
    return webpage

@app.route("/google")
def QueryFighterAircraft():
    ''' Query the database for fighter aircraft and return the results as a JSON. '''

    # Open a session, run the query, and then close the session again
    session = Session(engine)
    results = session.query(table.country, table.iso3, table.fighteraircraft).all()
    session.close()

    # Create a list of dictionaries, with each dictionary containing one row from the query. 
    all_aircraft = []
    for country, iso3, fighteraircraft in results:
        dict = {}
        dict["country"] = country
        dict["iso3"] = iso3
        dict["fighteraircraft"] = fighteraircraft
        all_aircraft.append(dict)

    # Return the jsonified result. 
    return jsonify(all_aircraft)

@app.route("/health")
def QueryPopulation():
    ''' Query the database for population numbers and return the results as a JSON. '''

    # Open a session, run the query, and then close the session again
    session = Session(engine)
    results = session.query(table.country, table.iso3, table.totalpopulation).all()
    session.close 

    # Create a list of dictionaries, with each dictionary containing one row from the query. 
    all_population = []
    for country, iso3, totalpopulation in results:
        dict = {}
        dict["country"] = country
        dict["iso3"] = iso3
        dict["totalpopulation"] = totalpopulation
        all_population.append(dict)

    # Return the jsonified result. 
    return jsonify(all_population)

@app.route("/test")
def TestRoute():
    ''' This function returns a simple message, just to guarantee that
        the Flask server is working. '''

    return "This is the test route!"



# This statement is required for Flask to do its job. 
# Think of it as chocolate cake recipe. 
if __name__ == '__main__':
    app.run(debug=True)