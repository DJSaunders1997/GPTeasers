import LoadingBar from "./loadingbar.js";

class UI {
  constructor() {
    this.topic = document.getElementById("quizTopic").value;
    this.button = document.querySelector("button");

    this.topicInput = document.getElementById("quizTopic");
    this.button = document.querySelector("button");

    this.quizContainer = document.getElementById("quiz-container");

    this.loadingBar = new LoadingBar();
    // ... Add other DOM elements you might want to manipulate.

    //Quiz elements
    this.questionText = document.getElementById("question-text");
    this.buttonA = document.getElementById("option-A");
    this.buttonB = document.getElementById("option-B");
    this.buttonC = document.getElementById("option-C");
    // Ensure this is hidden by default
    this.hideQuizContainer();
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

  showQuizContainer() {
    this.quizContainer.style.display = "block";
  }

  hideQuizContainer() {
    this.quizContainer.style.display = "none";
  }

  // Display question in ui elements
  // Example currentQuestion format:
  //     {
  //         "question_id": 1,
  //         "question": "What is the scientific name of domestic cats?",
  //         "A": "Felis catus",
  //         "B": "Canis lupus",
  //         "C": "Panthera leo",
  //         "answer": "A",
  //         "explanation": "The scientific name of domestic cats is Felis catus.",
  //         "wikipedia": "https://en.wikipedia.org/wiki/Domestic_cat",
  //         "dalle_prompt": "Image of a domestic cat"
  //     },
  displayCurrentQuestion(currentQuestion) {
    console.log("Showing questions:");
    console.log(currentQuestion);

    if (currentQuestion) {
      this.questionText.textContent = currentQuestion.question;
      this.buttonA.textContent = "A: " + currentQuestion.A;
      this.buttonB.textContent = "B: " + currentQuestion.B;
      this.buttonC.textContent = "C: " + currentQuestion.C;
    } else {
      console.error("No current question to display");
    }
  }
  // ... You can add more UI related methods as needed.
}

export default UI;
