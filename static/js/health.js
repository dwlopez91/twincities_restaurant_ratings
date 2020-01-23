// Adding tile layer
var map = L.map("map-id", {
  center: [44.9602, -93.2659],
  zoom: 13,
});

L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  zoom:13,
  maxZoom: 15,
  minZoom:13,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(map);

map.zoomControl.remove();

fetch('/health_data')
    .then(function (health_array) {
        return health_array.json(); // But parse it as JSON this time
    })
    .then(function (json) {
        console.log('GET response as JSON:');
        console.log(json); // Here's our JSON object
        // Create a circle and pass in some initial options
        for(i=0; i < json.length; i++) {
            var inspectionscore = json[i].inspectionscore
            function color_swap(inspectionscore){
              if (inspectionscore >= 95){
                  return 'green';
              } else if (inspectionscore >=90){
                  return 'yellowgreen';
              } else if (inspectionscore >= 85){
                  return "orange";
              } else {
                  return 'red';
              }}
                // //
            L.circle([json[i].latitude, json[i].longitude], {
                fillColor: color_swap(inspectionscore),
                fillOpacity: 0.5,
                color: "black",
                stroke:.0001,
                radius: 75
            }).addTo(map).bindPopup("<h2><center><u>" + json[i].businessname + "</u></center></h2><center><h3><i>" + json[i].fulladdress + "</i></h3></center><center><h4> Highest Health Inspection Score: " + json[i].inspectionscore +"</h4></center><center><h4>Date of Inspection:<br>" + json[i].dateifinspection +"</h4></center>")            
    }
  });

map.on('popupopen', function(centerMarker) {
  var cM = map.project(centerMarker.popup._latlng);
  cM.y -= centerMarker.popup._container.clientHeight/2
  map.setView(map.unproject(cM),15, {animate: true});
});

