import LoadingBar from "./loadingbar.js";
import { CSS_CLASSES} from "./config.js";
import DOMElements from "./domElements.js";

class UI {
  constructor() {
    this.elements = new DOMElements();
    this.loadingBar = new LoadingBar();
    
    // Ensure UI is hidden by default
    this.hideQuizContainer();
    this.hideFeedback();
  }

  // When loading show loading clues, disable quiz generation button, and show loading bar.
  showLoading() {
    console.log("Showing loading clues")
    document.body.style.cursor = "wait";
    this.elements.fetchButton.disabled = true;
    this.loadingBar.start();
  }

  // Stop loading elements
  hideLoading() {
    console.log("Hiding loading clues")
    document.body.style.cursor = "default";
    this.elements.fetchButton.disabled = false;
    this.loadingBar.stop();
  }

  showQuizContainer(quizTitle) {
    // Hide button inputs
    this.elements.inputContainer.style.display = "none"
    this.elements.intro.style.display = "none" 

    this.elements.quizContainer.style.display = "block";
    this.elements.quizTitle.textContent = quizTitle;
  }

  hideQuizContainer() {
    this.elements.quizContainer.style.display = "none";
  }

  hideFeedback() {
    if (this.elements.quizFeedback) {
      this.elements.quizFeedback.style.display = "none";
      this.elements.quizFeedback.innerHTML = "";
      this.elements.quizFeedback.classList.remove("feedback-final");
    }
  }

  showAIImage(data){
    this.elements.AIImage.style.display = "block"
    this.elements.AIImage.src = data;
  }

  hideAIImage(){
    this.elements.AIImage.style.display = "none"
  }

  getTopic(){
    return this.elements.topicInput.value;
  }

  getDifficulty(){
    return this.elements.quizDifficulty.value;
  }

  getModel() {
    return this.elements.quizModel.value;
  }

  /**
   * Updates the on-screen quiz meta strip with progress and score.
   * @param {number} currentQuestionNumber - 1-based index of the active question.
   * @param {number} totalQuestions - Total questions in the quiz.
   * @param {number} score - Current user score.
   */
  updateProgress(currentQuestionNumber, totalQuestions, score) {
    if (this.elements.quizProgress) {
      this.elements.quizProgress.textContent = `Question ${currentQuestionNumber} of ${totalQuestions}`;
    }
    if (this.elements.quizScore) {
      this.elements.quizScore.textContent = `Score: ${score}`;
    }
  }

  /**
   * Renders inline answer feedback (correctness, explanation, wiki link, and summary).
   * @param {Object} result - Structured answer result from Quiz.checkAnswer.
   */
  showAnswerFeedback(result) {
    if (!this.elements.quizFeedback) {
      return;
    }

    this.elements.quizFeedback.style.display = "block";
    this.elements.quizFeedback.innerHTML = "";

    const status = document.createElement("p");
    status.textContent = result.correct ? "Correct!" : "Wrong.";
    status.className = result.correct ? CSS_CLASSES.feedbackCorrect : CSS_CLASSES.feedbackWrong;
    this.elements.quizFeedback.appendChild(status);

    // Show answer choices with indication of selected and correct
    const choicesDiv = document.createElement("div");
    choicesDiv.className = CSS_CLASSES.feedbackChoices;
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
        choice.key === result.answer ? CSS_CLASSES.choiceCorrect : CSS_CLASSES.choiceNeutral;
      choicesDiv.appendChild(choiceP);
    });

    this.elements.quizFeedback.appendChild(choicesDiv);

    if (result.explanation) {
      const explanation = document.createElement("p");
      explanation.textContent = `Explanation: ${result.explanation}`;
      this.elements.quizFeedback.appendChild(explanation);
    }

    if (result.wikipedia) {
      const wikiLink = document.createElement("a");
      wikiLink.href = result.wikipedia;
      wikiLink.target = "_blank";
      wikiLink.rel = "noopener noreferrer";
      wikiLink.textContent = "Read more";
      this.elements.quizFeedback.appendChild(wikiLink);
    }

    const summary = document.createElement("p");
    summary.textContent = `Question ${result.questionNumber} of ${result.totalQuestions} • Score: ${result.score}`;
    this.elements.quizFeedback.appendChild(summary);
  }

  /**
   * Displays the final score summary and disables further inputs.
   * @param {Object} result - Final answer result payload from Quiz.checkAnswer.
   */
  showFinalScore(result) {
    this.showAnswerFeedback(result);
    this.elements.quizFeedback.classList.add(CSS_CLASSES.feedbackFinal);
    this.disableAnswerButtons();
    this.hideAnswerButtons();
    this.showNewQuizButton();
  }

  disableAnswerButtons() {
    this.elements.getAnswerButtons().forEach((button) => {
      if (button) {
        button.disabled = true;
      }
    });
  }

  /**
   * Hides answer option buttons (A, B, C).
   */
  hideAnswerButtons() {
    this.elements.getAnswerButtons().forEach((button) => {
      if (button) {
        button.style.display = "none";
      }
    });
  }

  /**
   * Shows answer option buttons (A, B, C) and re-enables them.
   */
  showAnswerButtons() {
    this.elements.getAnswerButtons().forEach((button) => {
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
    if (this.elements.nextQuestionButton) {
      this.elements.nextQuestionButton.style.display = "block";
    }
  }

  /**
   * Hides the Next Question button.
   */
  hideNextQuestionButton() {
    if (this.elements.nextQuestionButton) {
      this.elements.nextQuestionButton.style.display = "none";
    }
  }

  /**
   * Shows the New Quiz button.
   */
  showNewQuizButton() {
    if (this.elements.newQuizButton) {
      this.elements.newQuizButton.style.display = "block";
    }
  }

  /**
   * Hides the New Quiz button.
   */
  hideNewQuizButton() {
    if (this.elements.newQuizButton) {
      this.elements.newQuizButton.style.display = "none";
    }
  }

  /**
   * Render quiz history list from stored entries.
   * @param {Array} history - Array of quiz attempts.
   */
  renderHistory(history) {
    if (!this.elements.historySection || !this.elements.historyList) {
      return;
    }

    const hasHistory = Array.isArray(history) && history.length > 0;
    this.elements.historySection.style.display = hasHistory ? "block" : "none";

    if (this.elements.historyEmptyMessage) {
      this.elements.historyEmptyMessage.style.display = hasHistory ? "none" : "block";
    }

    this.elements.historyList.innerHTML = "";

    if (!hasHistory) {
      return;
    }

    history
      .slice()
      .reverse()
      .forEach((entry) => {
        const li = document.createElement("li");
        const date = entry.finishedAt
          ? new Date(entry.finishedAt).toLocaleString()
          : "";
        li.textContent = `${entry.topic || "(no topic)"} • ${entry.difficulty || ""} • ${entry.model || ""} • ${entry.score}/${entry.totalQuestions} • ${date}`;
        this.elements.historyList.appendChild(li);
      });
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
    this.elements.quizModel.innerHTML = '';
    
    // Create and add new options
    models.forEach(model => {
      const option = document.createElement('option');
      option.value = model;
      option.textContent = model;
      
      // Set as selected if it's the default model
      if (defaultModel && model === defaultModel) {
        option.selected = true;
      }
      
      this.elements.quizModel.appendChild(option);
    });
    
    // If no default was provided or found, select the first option
    if (!defaultModel && models.length > 0) {
      this.elements.quizModel.selectedIndex = 0;
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
      this.elements.questionText.textContent = currentQuestion.question;
      this.elements.buttonA.textContent = "A: " + currentQuestion.A;
      this.elements.buttonB.textContent = "B: " + currentQuestion.B;
      this.elements.buttonC.textContent = "C: " + currentQuestion.C;
    } else {
      console.error("No current question to display");
    }
  }
}

export default UI;
