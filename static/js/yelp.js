// console.log(yelp_reviews)

fetch('/yelp_data')
    .then(function (yelp_reviews) {
        return yelp_reviews.json(); // But parse it as JSON this time
    })
    .then(function (json) {
        console.log('GET response as JSON:');
        console.log(json[0]); // Here’s our JSON object
        console.log(json[0].latitude);

    });

// need a for loop to grab data from the array and put to variables?
