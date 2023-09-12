import LoadingBar from "./loadingbar.js";

class UI {
  constructor() {
    this.topic = document.getElementById("quizTopic").value;
    this.button = document.querySelector("button");

    this.topicInput = document.getElementById("quizTopic");
    this.button = document.querySelector("button");
    this.jsonResponseContainer = document.getElementById("jsonResponse");

    this.quizContainer = document.getElementById("quiz-container");

    this.loadingBar = new LoadingBar();
    // ... Add other DOM elements you might want to manipulate.

    // Ensure this is hidden by default
    this.hideQuizContainer()
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

  showQuizContainer()
  {
    this.quizContainer.style.display = 'block';
  }

  hideQuizContainer()
  {
    this.quizContainer.style.display = 'none';
  }

  displayQuizData(data) {
    this.jsonResponseContainer.textContent = JSON.stringify(data, null, 2);
    //TODO: Display responses as buttons n shit
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
      const questionText = document.getElementById("question-text");
      const buttonA = document.getElementById("option-A");
      const buttonB = document.getElementById("option-B");
      const buttonC = document.getElementById("option-C");

      questionText.textContent = currentQuestion.question;
      buttonA.textContent = "A: " + currentQuestion.A;
      buttonB.textContent = "B: " + currentQuestion.B;
      buttonC.textContent = "C: " + currentQuestion.C;
    } else {
      console.error("No current question to display");
    }
  }
  // ... You can add more UI related methods as needed.
}

export default UI;
