let interval;

function startLoadingBar(duration = 25000) {
    const loadingBar = document.getElementById('loadingBar');
    const loadingBarContainer = document.getElementById('loadingBarContainer');
    
    // Reset the bar
    loadingBar.style.width = '0%';
    
    // Show the bar container
    loadingBarContainer.style.display = 'block';
    
    let width = 0;
    interval = setInterval(function() {
        if (width >= 100) {
            clearInterval(interval);
        } else {
            width++;
            loadingBar.style.width = width + '%'; 
        }
    }, duration / 100);  // e.g., for 25000ms (25s), it will increase width every 250ms.
}

function stopLoadingBar() {
    clearInterval(interval);
    const loadingBar = document.getElementById('loadingBar');
    const loadingBarContainer = document.getElementById('loadingBarContainer');
    
    // Reset the bar
    loadingBar.style.width = '0%';
    
    // Hide the bar container
    loadingBarContainer.style.display = 'none';
}
