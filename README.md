# twincities_restaurant_ratings

To set up the back end:

    Files needed are in MinneapolisRestaurantBackend:

        1) Create empty folder called DataFiles in the folder.

        2) Create config.py in the folder with:
            api_key = {yelp api key}
            google_key = {google api key}

        3) Run the API_Dowloader.py python file

        4) In PostgresSQL, run the PostgresSQL_Schema script

        5) Upload the files from DataFiles to Postgres:
            GoogleData.csv
            InspectionsData.csv
            YelpData.csv