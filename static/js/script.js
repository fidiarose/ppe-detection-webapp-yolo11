document.addEventListener('DOMContentLoaded', function() {
    // Webcam Detection
    const startWebcamBtn = document.getElementById('startWebcam');
    const webcamFeed = document.getElementById('webcamFeed');

    startWebcamBtn.addEventListener('click', function() {
        webcamFeed.src = '/video_feed';
        webcamFeed.style.display = 'block';
    });
});
