function updateData() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            document.getElementById('temperature').textContent = `${data.temperature.toFixed(1)}°C`;
            document.getElementById('humidity').textContent = `${data.humidity.toFixed(1)}%`;
        });
}

function captureImage() {
    fetch('/capture')
        .then(response => response.blob())
        .then(blob => {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(blob);
            document.getElementById('gallery').prepend(img);
        });
}

function loadImages() {
    fetch('/images')
        .then(response => response.json())
        .then(data => {
            const gallery = document.getElementById('gallery');
            data.images.forEach(filename => {
                const img = document.createElement('img');
                img.src = `/image/${filename}`;
                gallery.appendChild(img);
            });
        });
}

window.onload = function() {
    updateData();
    setInterval(updateData, 10000);  // Update data every minute
    // loadImages();
}

