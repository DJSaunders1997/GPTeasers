/**
 * This file contains functions related to the GPTeasers Quiz App.
 * It manages the fetching of quiz data from the API and its presentation on the web page.
 */
import Controller from "./controller.js";
import UI from "./ui.js";
import Quiz from "./quiz.js";

class App {
  constructor() {
    // Initialise app elements as JS objects.
    this.quiz = null; // created on demand per quiz run
    this.controller = new Controller();
    this.ui = new UI();
    this.quizHistory = this.loadQuizHistory();
    this.currentTopic = "";
    this.currentDifficulty = "";
    this.currentModel = "";

    // Render any existing history on load
    this.ui.renderHistory(this.quizHistory);

    // Initialize mobile menu toggle
    this.initMobileMenu();

    // Load supported models dynamically
    this.loadSupportedModels();

    // Initialise button event listeners
    this.bindButtonEvents();
    this.bindEnterKeyToQuizButton();
  }

  /**
   * Bind event listeners to quiz control buttons.
   * @private
   */
  bindButtonEvents() {
    this.ui.elements.fetchButton.addEventListener("click", () => this.fetchQuizData());
    this.ui.elements.fetchButton.addEventListener("click", () => this.fetchAIImage());
    this.ui.elements.buttonA.addEventListener("click", () => this.checkAnswer("A"));
    this.ui.elements.buttonB.addEventListener("click", () => this.checkAnswer("B"));
    this.ui.elements.buttonC.addEventListener("click", () => this.checkAnswer("C"));
    this.ui.elements.nextQuestionButton.addEventListener("click", () => this.nextQuestion());
    this.ui.elements.newQuizButton.addEventListener("click", () => location.reload());
  }

  /**
   * Bind Enter key on quiz topic input to trigger quiz generation.
   * @private
   */
  bindEnterKeyToQuizButton() {
    this.ui.elements.topicInput.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        this.ui.elements.fetchButton.click();
        }
      });
  }

  /**
   * Initialize mobile menu toggle functionality
   */
  initMobileMenu() {
    const navbarToggle = this.ui.elements.navbarToggle;
    const navbarLinks = this.ui.elements.navbarLinks;
    
    if (navbarToggle && navbarLinks) {
      navbarToggle.addEventListener('click', () => {
        navbarLinks.classList.toggle('active');
        
        // Add animation to hamburger menu
        navbarToggle.classList.toggle('active');
      });

      // Close mobile menu when clicking on a link
      navbarLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
          navbarLinks.classList.remove('active');
          navbarToggle.classList.remove('active');
        });
      });

      // Close mobile menu when clicking outside
      document.addEventListener('click', (event) => {
        if (!navbarToggle.contains(event.target) && !navbarLinks.contains(event.target)) {
          navbarLinks.classList.remove('active');
          navbarToggle.classList.remove('active');
        }
      });
    }
  }

  async fetchQuizData() {
    // Get the topic and difficulty from the input field
    const topic = this.ui.getTopic();
    const difficulty = this.ui.getDifficulty();
    const model = this.ui.getModel();
    const numQuestions = this.ui.getNumQuestions();

    // Persist current quiz metadata for history logging
    this.currentTopic = topic;
    this.currentDifficulty = difficulty;
    this.currentModel = model;

    // Create fresh quiz state with requested number of questions
    this.quiz = new Quiz(numQuestions);
    this.controller.quiz = this.quiz;
    this.controller.numQuestions = numQuestions;

    // Check if topic is empty or contains only whitespace
    if (!topic.trim()) {
      alert("Please enter a valid topic.");
      return; // Exit the function early without further processing
    }

    // Show loading clues
    this.ui.showLoading();

    try {
      // Flag to check if it's the first question
      let firstQuestionReceived = false;

      // Generate Quiz
      // The await keyword is used to wait for the asynchronous callQuizAPI method to complete.
      // This means the code execution will pause here until callQuizAPI returns a result or throws an error.
      // It's like telling JavaScript to wait here and don't move to the next line until this promise is resolved.
      // use the onQuestionReceived callback to display each question individually as it is added to the Quiz object.
      // Arrow function: Shorter syntax for functions and keeps 'this' context from surrounding code
      // Set's up quiz only when the first question is received
      await this.controller.callQuizAPI(topic, difficulty, model, () => {
        if(!firstQuestionReceived){
          this.showQuestion(); // Question should've been added to quiz, so display it
          this.ui.hideLoading(); // Hide loading clues
          this.ui.showQuizContainer(topic); // Show quiz container
        }
        // If the first question has been received, then don't show it again
        firstQuestionReceived = true;
      });
    } catch (error) {
      console.error("Error fetching quiz data:", error);
      alert("Failed to fetch quiz data. Please try again.");
      this.ui.hideLoading();
    }
  }

  async fetchAIImage() {
    // Use the topic as a prompt to image
    const prompt = this.ui.elements.topicInput.value;

    // Check if prompt is empty or contains only whitespace
    if (!prompt.trim()) {
      alert("Please enter a valid prompt.");
      return; // Exit the function early without further processing
    }

    try {
      // Fetch Image
      // The await keyword is used to wait for the asynchronous callImageAPI method to complete.
      // This means the code execution will pause here until the call returns a result or throws an error.
      // It's like telling JavaScript to wait here and don't move to the next line until this promise is resolved.
      const data = await this.controller.callImageAPI(prompt);
      if (!data || data.error) {
        throw new Error("Invalid data received from Image API");
      }

      // Display Image
      this.ui.showAIImage(data);
    } catch (error) {
      console.error("Error fetching AI image:", error);
      alert("Failed to fetch AI image. Please try again.");
    }
  }

  showQuestion() {
    // Get question from quiz
    const question = this.quiz.getCurrentQuestion();
    // Update UI elements
    this.ui.displayCurrentQuestion(question);
    this.ui.updateProgress(this.quiz.currentIndex + 1, this.quiz.numQuestions, this.quiz.score);
  }

  // Calls quiz check answer method
  // and displays the next question
  /**
   * Handles answer selection, renders inline feedback, and advances quiz flow.
   * @param {"A"|"B"|"C"} answer - Selected option key.
   */
  checkAnswer(answer) {
    const result = this.quiz.checkAnswer(answer);

    if (!result) {
      return;
    }

    if (result.isFinished) {
      this.saveQuizResult(result);
      this.ui.showFinalScore(result);
      this.ui.updateProgress(this.quiz.numQuestions, this.quiz.numQuestions, this.quiz.score);
      return;
    }

    this.ui.hideAnswerButtons();
    this.ui.showAnswerFeedback(result);
    this.ui.showNextQuestionButton();
  }

  nextQuestion() {
    this.ui.hideFeedback();
    this.ui.hideNextQuestionButton();
    this.ui.hideNewQuizButton();
    this.ui.showAnswerButtons();
    this.showQuestion();
  }

  /**
   * Loads the supported models from the backend API and populates the dropdown.
   * Called during app initialization to ensure the dropdown is dynamically populated.
   */
  async loadSupportedModels() {
    try {
      console.log("Loading supported models from backend...");
      const models = await this.controller.fetchSupportedModels();
      
      if (models && models.length > 0) {
        // Use gpt-3.5-turbo as default 
        const defaultModel = "gpt-3.5-turbo";
        this.ui.populateModelDropdown(models, defaultModel);
        console.log("Successfully populated model dropdown");
      } else {
        console.warn("No supported models received from backend");
      }
    } catch (error) {
      console.error("Failed to load supported models:", error);
      // Don't alert the user as this is a background operation
      // The dropdown will keep its existing hardcoded options if this fails
    }
  }

  /**
   * Retrieve quiz history from localStorage.
   * @returns {Array} Stored quiz attempts.
   */
  loadQuizHistory() {
    try {
      const raw = localStorage.getItem("gptQuizHistory");
      return raw ? JSON.parse(raw) : [];
    } catch (error) {
      console.warn("Failed to load quiz history from localStorage", error);
      return [];
    }
  }

  /**
   * Append the current quiz result to localStorage history.
   * @param {Object} result - Final quiz result payload.
   */
  saveQuizResult(result) {
    const entry = {
      topic: this.currentTopic,
      difficulty: this.currentDifficulty,
      model: this.currentModel,
      score: result.score,
      totalQuestions: result.totalQuestions,
      finishedAt: new Date().toISOString(),
    };

    try {
      const history = this.loadQuizHistory();
      history.push(entry);
      localStorage.setItem("gptQuizHistory", JSON.stringify(history));
      this.quizHistory = history;
      this.ui.renderHistory(history);
    } catch (error) {
      console.warn("Failed to save quiz history to localStorage", error);
    }
  }

  /**
   * Clear quiz history from localStorage and UI.
   */
  clearQuizHistory() {
    try {
      localStorage.removeItem("gptQuizHistory");
      this.quizHistory = [];
      this.ui.renderHistory([]);
    } catch (error) {
      console.warn("Failed to clear quiz history", error);
    }
  }
}

const app = new App();
