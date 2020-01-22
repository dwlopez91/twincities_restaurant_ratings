var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
  zoom: 22,
  id: "mapbox.light",
  accessToken: API_KEY
});

// Initialize all of the LayerGroups we'll be using
var layers = {
  Yelp: new L.LayerGroup(),
  Google: new L.LayerGroup(),
  Health: new L.LayerGroup(),

};

// Create the map with our layers
var map = L.map("map-id", {
  center: [44.9602, -93.2659],
  zoom: 12,
  layers: [
    layers.Yelp,
    layers.Google,
    layers.Health
  ]
});

// Add our 'lightmap' tile layer to the map
lightmap.addTo(map);

var overlays = {
  "Yelp": layers.Yelp,
  "Google": layers.Google,
  "Health Inspections": layers.Health
};

L.control.layers(null, overlays).addTo(map);

fetch('/yelp_data')
    .then(function (yelp_reviews) {
        return yelp_reviews.json(); // But parse it as JSON this time
    })
    .then(function (json) {
        console.log('GET response as JSON:');
        console.log(json); // Here’s our JSON object
        // Create a circle and pass in some initial options
        for(i=0; i < json.length; i++) {
            L.circle([json[i].latitude, json[i].longitude], {
                fillColor: "green",
                opacity: 0.5,
                color: "black",
                fillOpacity: 0.5,
                radius: (json[i].reviews/5)
            }).addTo(map).bindPopup("<h2><center><u>" + json[i].yelp_name + "</u></center></h2><center><h3><i>" + json[i].address + "</i></h3></center><center><h4> Yelp Rating: " + json[i].rating +"</h4></center><center><h4>" + json[i].reviews + " Yelp reviews</h4></center>")
    }});

// need a for loop to grab data from the array and put to variables?
