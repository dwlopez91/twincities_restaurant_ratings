// console.log(yelp_reviews)

fetch('/yelp_data')
    .then(function (results) {
        return results.json(); // But parse it as JSON this time
    })
    .then(function (json) {
        console.log('GET response as JSON:');
        console.log(json); // Here’s our JSON object
    });

    