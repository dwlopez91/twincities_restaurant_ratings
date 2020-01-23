# twincities_restaurant_ratings

To set up the back end:

    Files needed are in MinneapolisRestaurantBackend:

        1) Create config.py in the folder with:
            api_key = {yelp api key}
            google_key = {google api key}

        2) Create an empty folder called DataFiles in the folder.

        3) Run the API_Dowloader.py python file in the terminal.
        
        4) In PostgresSQL, run the PostgresSQL_Schema script.
        
        5) Upload the files from DataFiles to Postgres:
            GoogleData.csv
            InspectionsData.csv
            YelpData.csv
        
        6) In PostgresSQL, run the CleanInspectionData query inside the table 'InspectionData'
        
        7) Download the query results as a CSV and remove the header.
        
        8) In PostgresSQL, run the CleanDataInspection schema script.
        
        9) Upload CleandInspectionData.csv to Postgres.