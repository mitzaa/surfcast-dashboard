window.onload = function() {
    fetch(`/surfcast?lat=${latitude}&lon=${longitude}`)  
    .then(response => response.json())
    .then(data => {
       
        let waveHeight = data.hours[0].waveHeight.sg;  
        let windSpeed = data.hours[0].windSpeed.sg;
        let swellDirection = data.hours[0].swellDirection.sg;

        document.getElementById('waveHeight').textContent = waveHeight + ' m';
        document.getElementById('windSpeed').textContent = windSpeed + ' m/s';
        document.getElementById('swellDirection').textContent = swellDirection + '°';
    })
    .catch(error => {
        console.error("There was an error fetching the surf data:", error);
    });
};
