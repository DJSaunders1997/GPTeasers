import LoadingBar from "./loadingbar.js";

class UI {
  constructor() {
    this.inputContainer = document.getElementById("inputContainer");
    this.intro = document.getElementById("intro");
    this.topicInput = document.getElementById("quizTopic");
    this.quizDifficulty = document.getElementById("quizDifficulty");
    this.button = document.querySelector("button");

    //Image elements
    this.AIImage = document.getElementById("AIImage");

    this.loadingBar = new LoadingBar();
    
    //Quiz elements
    this.quizContainer = document.getElementById("quiz-container");
    this.quizTitle = document.getElementById("quizTitle");
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

  showQuizContainer(quizTitle) {

    // Hide button inputs
    this.inputContainer.style.display = "none"
    this.intro.style.display = "none" 

    this.quizContainer.style.display = "block";
    this.quizTitle.textContent = quizTitle;
  }

  hideQuizContainer() {
    this.quizContainer.style.display = "none";
  }

  showAIImage(data){
    this.AIImage.style.display = "block"
    this.AIImage.src = data;
  }

  hideAIImage(){
    this.AIImage.style.display = "none"
  }

  getTopic(){
    return this.topicInput.value;
  }

  getDifficulty(){
    return this.quizDifficulty.value;
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
}

export default UI;
