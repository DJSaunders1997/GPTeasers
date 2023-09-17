/**
 * Class representing a loading bar.
 */
class LoadingBar {
  constructor() {
    this.interval = null;
    this.loadingBar = document.getElementById("loadingBar");
    this.loadingBarContainer = document.getElementById("loadingBarContainer");
  }

  /**
   * Start the loading bar animation.
   * @param {number} [duration=60000] - Duration in milliseconds for the loading bar to complete.
   */
  start(duration = 60000) {
    // Reset the bar
    this.loadingBar.style.width = "0%";

    // Show the bar container
    this.loadingBarContainer.style.display = "block";

    let width = 0;
    this.interval = setInterval(() => {
      if (width >= 100) {
        clearInterval(this.interval);
      } else {
        width++;
        this.loadingBar.style.width = width + "%";
      }
    }, duration / 100); // e.g., for 60000ms (60s), it will increase width every 600ms.
  }

  /**
   * Stop the loading bar animation and hide it.
   */
  stop() {
    clearInterval(this.interval);

    // Reset the bar
    this.loadingBar.style.width = "0%";

    // Hide the bar container
    this.loadingBarContainer.style.display = "none";
  }
}

export default LoadingBar;
