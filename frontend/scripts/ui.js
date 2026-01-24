import LoadingBar from "./loadingbar.js";

class UI {
  constructor() {
    this.inputContainer = document.getElementById("inputContainer");
    this.intro = document.getElementById("intro");
    this.topicInput = document.getElementById("quizTopic");
    this.quizDifficulty = document.getElementById("quizDifficulty");
    this.quizModel = document.getElementById("quizModel")
    this.button = document.querySelector("button");

    //Image elements
    this.AIImage = document.getElementById("AIImage");

    this.loadingBar = new LoadingBar();
    
    //Quiz elements
    this.quizContainer = document.getElementById("quiz-container");
    this.quizTitle = document.getElementById("quizTitle");
    this.quizProgress = document.getElementById("quizProgress");
    this.quizScore = document.getElementById("quizScore");
    this.questionText = document.getElementById("question-text");
    this.quizFeedback = document.getElementById("quizFeedback");
    this.buttonA = document.getElementById("option-A");
    this.buttonB = document.getElementById("option-B");
    this.buttonC = document.getElementById("option-C");
    // Ensure this is hidden by default
    this.hideQuizContainer();
    this.hideFeedback();
  }

  // When loading show loading clues, disable quiz generation button, and show loading bar.
  showLoading() {
    console.log("Showing loading clues")
    document.body.style.cursor = "wait";
    this.button.disabled = true;
    this.loadingBar.start();
  }

  // Stop loading elements
  hideLoading() {
    console.log("Hiding loading clues")
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

  hideFeedback() {
    if (this.quizFeedback) {
      this.quizFeedback.style.display = "none";
      this.quizFeedback.innerHTML = "";
      this.quizFeedback.classList.remove("feedback-final");
    }
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

  getModel() {
    return this.quizModel.value;
  }

  /**
   * Updates the on-screen quiz meta strip with progress and score.
   * @param {number} currentQuestionNumber - 1-based index of the active question.
   * @param {number} totalQuestions - Total questions in the quiz.
   * @param {number} score - Current user score.
   */
  updateProgress(currentQuestionNumber, totalQuestions, score) {
    if (this.quizProgress) {
      this.quizProgress.textContent = `Question ${currentQuestionNumber} of ${totalQuestions}`;
    }
    if (this.quizScore) {
      this.quizScore.textContent = `Score: ${score}`;
    }
  }

  /**
   * Renders inline answer feedback (correctness, explanation, wiki link, and summary).
   * @param {Object} result - Structured answer result from Quiz.checkAnswer.
   */
  showAnswerFeedback(result) {
    if (!this.quizFeedback) {
      return;
    }

    this.quizFeedback.style.display = "block";
    this.quizFeedback.innerHTML = "";

    const status = document.createElement("p");
    status.textContent = result.correct ? "Correct!" : "Wrong.";
    status.className = result.correct ? "feedback-correct" : "feedback-wrong";
    this.quizFeedback.appendChild(status);

    // Show answer choices with indication of selected and correct
    const choicesDiv = document.createElement("div");
    choicesDiv.className = "feedback-choices";
    const choices = [
      { key: "A", value: result.optionA },
      { key: "B", value: result.optionB },
      { key: "C", value: result.optionC },
    ];

    choices.forEach((choice) => {
      const choiceP = document.createElement("p");
      let marker = "";
      if (choice.key === result.selected) {
        marker += " ← Your answer";
      }
      if (choice.key === result.answer) {
        marker += " ✓ Correct";
      }
      choiceP.textContent = `${choice.key}: ${choice.value}${marker}`;
      choiceP.className =
        choice.key === result.answer ? "choice-correct" : "choice-neutral";
      choicesDiv.appendChild(choiceP);
    });

    this.quizFeedback.appendChild(choicesDiv);

    if (result.explanation) {
      const explanation = document.createElement("p");
      explanation.textContent = `Explanation: ${result.explanation}`;
      this.quizFeedback.appendChild(explanation);
    }

    if (result.wikipedia) {
      const wikiLink = document.createElement("a");
      wikiLink.href = result.wikipedia;
      wikiLink.target = "_blank";
      wikiLink.rel = "noopener noreferrer";
      wikiLink.textContent = "Read more";
      this.quizFeedback.appendChild(wikiLink);
    }

    const summary = document.createElement("p");
    summary.textContent = `Question ${result.questionNumber} of ${result.totalQuestions} • Score: ${result.score}`;
    this.quizFeedback.appendChild(summary);
  }

  /**
   * Displays the final score summary and disables further inputs.
   * @param {Object} result - Final answer result payload from Quiz.checkAnswer.
   */
  showFinalScore(result) {
    this.showAnswerFeedback(result);
    this.quizFeedback.classList.add("feedback-final");
    this.disableAnswerButtons();
  }

  disableAnswerButtons() {
    [this.buttonA, this.buttonB, this.buttonC].forEach((button) => {
      if (button) {
        button.disabled = true;
      }
    });
  }

  /**
   * Hides answer option buttons (A, B, C).
   */
  hideAnswerButtons() {
    [this.buttonA, this.buttonB, this.buttonC].forEach((button) => {
      if (button) {
        button.style.display = "none";
      }
    });
  }

  /**
   * Shows answer option buttons (A, B, C) and re-enables them.
   */
  showAnswerButtons() {
    [this.buttonA, this.buttonB, this.buttonC].forEach((button) => {
      if (button) {
        button.style.display = "block";
        button.disabled = false;
      }
    });
  }

  /**
   * Shows the Next Question button.
   */
  showNextQuestionButton() {
    const nextBtn = document.getElementById("nextQuestionButton");
    if (nextBtn) {
      nextBtn.style.display = "block";
    }
  }

  /**
   * Hides the Next Question button.
   */
  hideNextQuestionButton() {
    const nextBtn = document.getElementById("nextQuestionButton");
    if (nextBtn) {
      nextBtn.style.display = "none";
    }
  }

  /**
   * Populates the model dropdown with the provided list of models.
   * Clears existing options and creates new ones.
   *
   * @param {Array} models - Array of model names from the backend
   * @param {string} defaultModel - Optional default model to select
   */
  populateModelDropdown(models, defaultModel = null) {
    console.log("Populating model dropdown with:", models);
    
    // Clear existing options
    this.quizModel.innerHTML = '';
    
    // Create and add new options
    models.forEach(model => {
      const option = document.createElement('option');
      option.value = model;
      option.textContent = model;
      
      // Set as selected if it's the default model
      if (defaultModel && model === defaultModel) {
        option.selected = true;
      }
      
      this.quizModel.appendChild(option);
    });
    
    // If no default was provided or found, select the first option
    if (!defaultModel && models.length > 0) {
      this.quizModel.selectedIndex = 0;
    }
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
    console.log("Showing question: ", currentQuestion);

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
