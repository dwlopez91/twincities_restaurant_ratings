var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
  maxZoom: 18,
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
  center: [44.9778, -93.2650],
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

// ** //

// var ricons = {
//   Yelp: L.ExtraMarkers.icon({
//     icon: "tbd/ yelp icon", 
//     iconColor: "Red",
//     markerColor: "tbd",
//     shape: "tbd"
//   }),

//   Google: L.ExtraMarkers.icon({
//     icon: "tbd/google icon",
//     iconColor: "Green", 
//     markerColor: "tbd", 
//     shape: "tbd"
//   }),

//   Health: L.ExtraMarkers.icon({
//     icon: "tbd",
//     iconColor:"Blue",
//     markerColor: "tbd",
//     shape: "tbd"
//   }),
// };




