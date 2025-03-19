(() => {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
    })
})()

const heatmapForm = document.querySelector("#heatmap-form");
const dayInput = document.querySelector("#heatmap-select-holiday");

var points = { data: [] };

// Gets the heatmap data points
async function getData() {
    const day = dayInput.value;
    const startTime = document.querySelector("#heatmap-start-time").value;
    const endTime = document.querySelector("#heatmap-end-time").value;

    const response = await fetch("/get_data",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                day: day,
                startTime: startTime,
                endTime: endTime
            })
        });
    const dataPoints = await response.json();
    points.data = [];
    for (const dataPoint of dataPoints) {
        points.data.push({ count: dataPoint[0], lat: dataPoint[1], lng: dataPoint[2] });
    }
    heatmapLayer.setData(points);
}

heatmapForm.addEventListener("submit", e => {
    e.preventDefault();
    // End value must be strictly greater than start value
    if (parseInt(endTime.value) <= parseInt(startTime.value)) {
        alert("End time must be greater than start time");
        return;
    }
    getData();
});

window.addEventListener("load", e => {
    getData();
});

const startTime = document.querySelector("#heatmap-start-time");
const endTime = document.querySelector("#heatmap-end-time");

const startTimeDisplay = document.querySelector("#start-time-display");
const endTimeDisplay = document.querySelector("#end-time-display");

const startLatitude = document.querySelector("#start-latitude");
const startLongitude = document.querySelector("#start-longitude");

const destinationLatitude = document.querySelector("#destination-latitude");
const destinationLongitude = document.querySelector("#destination-longitude");

// Displays the start time selected by the user
startTime.addEventListener("input", e => {
    startTimeDisplay.innerText = `${startTime.value}:00`;
});

// Displays the end time selected by the user
endTime.addEventListener("input", e => {
    endTimeDisplay.innerText = `${endTime.value}:00`;
});

const findStartLocation = document.querySelector("#find-start-location");
const findDestination = document.querySelector("#find-destination");
let finding = "";

// Starts the process of finding the start location
findStartLocation.addEventListener("click", e => {
    e.preventDefault();
    finding = "start";
    findStartLocation.innerText = "Finding Start Location";
});

// Starts the process of finding the destinaton
findDestination.addEventListener("click", e => {
    e.preventDefault();
    finding = "dest";
    findDestination.innerText = "Finding Destination";

});


let startMarker;
let destinationMarker;

var baseLayer = L.tileLayer(
    'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}
);

var cfg = {
    // radius should be small ONLY if scaleRadius is true (or small radius is intended)
    // if scaleRadius is false it will be the constant radius used in pixels
    "radius": 0.006,
    "maxOpacity": .8,
    // scales the radius based on map zoom
    "scaleRadius": true,
    // if set to false the heatmap uses the global maximum for colorization
    // if activated: uses the data maximum within the current map boundaries
    //   (there will always be a red spot with useLocalExtremas true)
    "useLocalExtrema": true,
    // which field name in your data represents the latitude - default "lat"
    latField: 'lat',
    // which field name in your data represents the longitude - default "lng"
    lngField: 'lng',
    // which field name in your data represents the data value - default "value"
    valueField: 'count'
};


var heatmapLayer = new HeatmapOverlay(cfg);

var map = new L.Map('map-canvas', {
    center: new L.LatLng(53.345481, -6.275819),
    zoom: 11,
    layers: [baseLayer, heatmapLayer]
});

// Handles click events on the map
map.on('click', function (e) {
    if (finding === "start") {
        finding = "";
        startLatitude.value = e.latlng.lat;
        startLongitude.value = e.latlng.lng;

        // Display temporary message to user
        findStartLocation.innerText = "Start Location Found!";

        // Adds marker to the map
        if (startMarker) {
            map.removeLayer(startMarker);
        }
        startMarker = L.marker([startLatitude.value, startLongitude.value]).addTo(map);

        // Remove temporary message after 1.5 seconds
        setTimeout(() => {
            findStartLocation.innerText = "Find Start Location";
        }, 1500);
    } else if (finding === "dest") {
        finding = "";
        destinationLatitude.value = e.latlng.lat;
        destinationLongitude.value = e.latlng.lng;

        // Display temporary message to user
        findDestination.innerText = "Destination Found!";

        // Adds marker to the map
        if (destinationMarker) {
            map.removeLayer(destinationMarker);
        }
        destinationMarker = L.marker([destinationLatitude.value, destinationLongitude.value]).addTo(map);

        // Remove temporary message after 1.5 seconds
        setTimeout(() => {
            findDestination.innerText = "Find Destination";
        }, 1500);
    }
});


// Adds marker on latitude and longitude input change
startLatitude.addEventListener("input", e => {
    if (!startLongitude.value) {
        return;
    }

    if (startMarker) {
        map.removeLayer(startMarker);
    }
    if (!isNaN(startLatitude.value) && !isNaN(startLongitude.value)) {
        startMarker = L.marker([startLatitude.value, startLongitude.value]).addTo(map);
    }
});

// Checks if values are invalid
startLatitude.addEventListener("blur", e => {
    if (isNaN(startLatitude.value)) {
        alert("Please input a valid latitude value");
    }
});

startLongitude.addEventListener("input", e => {


    if (!startLatitude.value) {
        return
    }

    if (startMarker) {
        map.removeLayer(startMarker);
    }
    if (!isNaN(startLatitude.value) && !isNaN(startLongitude.value)) {
        startMarker = L.marker([startLatitude.value, startLongitude.value]).addTo(map);
    }
});

startLongitude.addEventListener("blur", e => {
    if (isNaN(startLongitude.value)) {
        alert("Please input a valid longitude value");
    }
});

destinationLatitude.addEventListener("input", e => {

    if (!destinationLongitude.value) {
        return
    }
    if (destinationMarker) {
        map.removeLayer(destinationMarker);
    }
    if (!isNaN(destinationLatitude.value) && !isNaN(destinationLongitude.value)) {
        destinationMarker = L.marker([destinationLatitude.value, destinationLongitude.value]).addTo(map);
    }
});


destinationLatitude.addEventListener("blur", e => {
    if (isNaN(destinationLatitude.value)) {
        alert("Please input a valid latitude value");
    }
});

destinationLongitude.addEventListener("input", e => {
    if (!destinationLatitude.value) {
        return
    }
    if (destinationMarker) {
        map.removeLayer(destinationMarker);
    }
    if (!isNaN(destinationLatitude.value) && !isNaN(destinationLongitude.value)) {
        destinationMarker = L.marker([destinationLatitude.value, destinationLongitude.value]).addTo(map);
    }
});

destinationLongitude.addEventListener("blur", e => {
    if (isNaN(destinationLongitude.value)) {
        alert("Please input a valid longitude value");
    }
});


const pathfindForm = document.querySelector("#pathfind-form");
let path;
pathfindForm.addEventListener("submit", async e => {
    e.preventDefault();
    if (isNaN(startLongitude.value) || isNaN(startLatitude.value) || isNaN(destinationLongitude.value) || isNaN(destinationLatitude.value)) {
        alert("Please input valid latitude and longitude values");
        return;
    }
    const response = await fetch("/pathfind", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            data: points.data,
            startLatitude: startLatitude.value,
            startLongitude: startLongitude.value,
            destinationLatitude: destinationLatitude.value,
            destinationLongitude: destinationLongitude.value
        })
    });

    const result = await response.json();
    if (result.status === "error") {
        alert("An error occurred while finding the path. Message: " + result.message);
        return;
    }
    if (path) {
        path.removeFrom(map);
    }
    path = new L.Polyline(result.path, {
        color: 'blue',
        weight: 3,
        opacity: 0.5,
        smoothFactor: 1
    }).addTo(map);
});


const feedbackButtons = document.querySelectorAll("#feedback-buttons button");

feedbackButtons.forEach(button => {
    button.addEventListener("click", async e => {
        if (parseInt(endTime.value) <= parseInt(startTime.value)) {
            alert("End time must be greater than start time");
            return;
        }
        if (!startLongitude.value || !startLatitude.value || !destinationLongitude.value || !destinationLatitude.value) {
            alert("Please input latitude and longitude values");
            return;
        }
        if (isNaN(startLongitude.value) || isNaN(startLatitude.value) || isNaN(destinationLongitude.value) || isNaN(destinationLatitude.value)) {
            alert("Please input valid latitude and longitude values");
            return;
        }
        const response = await fetch("/feedback", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                helpful: (e.target.id === "feedback-yes") ? true : false,
                startLatitude: startLatitude.value,
                startLongitude: startLongitude.value,
                destinationLatitude: destinationLatitude.value,
                destinationLongitude: destinationLongitude.value,
                startTime: startTime.value,
                endTime: endTime.value,
                day: dayInput.value,
                submitTime: new Date().toLocaleString()
            })
        });

        const result = await response.json();
        if (result.status === "success") {
            alert("Thank you for your feedback!");
        } else {
            alert("An error occurred while submitting feedback. Message: " + result.message);
        }
    });
});
