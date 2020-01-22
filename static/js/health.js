
fetch('/health_data')
.then(function (health_array) {
    return health_array.json(); // But parse it as JSON this time
})
.then(function (json) {
    console.log('GET response as JSON:');
    console.log(json);

});

// need a for loop to grab data from the array and put to variables?