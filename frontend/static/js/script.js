document.addEventListener("DOMContentLoaded", function() {
    // Add an event listener to the button to fetch surfcast data when clicked
    document.getElementById("fetchData").addEventListener("click", function() {
        // Get lat and lon values from input fields
        const lat = document.getElementById("latitude").value;
        const lon = document.getElementById("longitude").value;

        // Ensure that lat and lon are not empty
        if (!lat || !lon) {
            alert("Please enter both latitude and longitude.");
            return;
        }

        // Fetch surfcast data using the provided lat and lon from backend on port 5001
        fetch(`http://localhost:5001/surfcast?lat=${lat}&lon=${lon}`)
            .then(response => response.json())
            .then(data => {
                const surfData = data.hours[0];  // Get the first hour data
                document.getElementById("waveHeight").textContent = "Wave Height: " + surfData.waveHeight.sg + " meters";
                document.getElementById("windSpeed").textContent = "Wind Speed: " + surfData.windSpeed.sg + " m/s";
                document.getElementById("swellDirection").textContent = "Swell Direction: " + surfData.swellDirection.sg + "°";
            })
            .catch(error => {
                console.error("Error fetching surfcast data:", error);
            });
    });
});


