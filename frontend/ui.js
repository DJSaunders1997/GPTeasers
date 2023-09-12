import LoadingBar from "./loadingbar.js";

class UI {
  constructor() {
    this.topic = document.getElementById("quizTopic").value;
    this.button = document.querySelector("button");

    this.topicInput = document.getElementById("quizTopic");
    this.button = document.querySelector("button");
    this.jsonResponseContainer = document.getElementById("jsonResponse");

    this.loadingBar = new LoadingBar();
    // ... Add other DOM elements you might want to manipulate.
  }

  // When loading show loading curson, disable quiz generation button, and show loading bar.
  showLoading() {
    document.body.style.cursor = "wait";
    this.button.disabled = true;
    this.loadingBar.start();
  }

  // Stop loading elements
  hideLoading() {
    document.body.style.cursor = "default";
    this.button.disabled = false;
    this.loadingBar.stop();
  }

  displayQuizData(data) {
    this.jsonResponseContainer.textContent = JSON.stringify(data, null, 2);

    //TODO: Display responses as buttons n shit
  }

  // ... You can add more UI related methods as needed.
}

export default UI;
