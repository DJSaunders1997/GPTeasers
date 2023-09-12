/**
 * This file contains functions related to the GPTeasers Quiz App.
 * It manages the fetching of quiz data from the API and its presentation on the web page.
 */
import Controller from "./controller.js";
import Game from "./game.js";
import UI from "./ui.js";
import Quiz from "./quiz.js";

class App {
  constructor() {
    // Initialise app elements as JS objects.
    this.controller = new Controller();
    this.ui = new UI();
    this.game = new Game(this.ui);

    // Initialise button event listener.
    // The arrow function implicitly binds the method to the current instance of this class.
    document
      .querySelector("#fetchQuizButton")
      .addEventListener("click", () => this.fetchQuizData());

    // If Enter key is pressed then simulate button press
    document
      .getElementById("quizTopic")
      .addEventListener("keydown", function (event) {
        // Check if the pressed key was the Enter key
        if (event.key === "Enter") {
          event.preventDefault(); // Prevent any default action
          document.querySelector("#fetchQuizButton").click(); // Simulate a click on the button
        }
      });
  }

  async fetchQuizData() {
    // Get the topic from the input field
    const topic = document.getElementById("quizTopic").value;

    // Check if topic is empty or contains only whitespace
    if (!topic.trim()) {
      alert("Please enter a valid topic.");
      return; // Exit the function early without further processing
    }

    // Show loading clues
    this.ui.showLoading();

    // Generate Quiz
    const data = await this.controller.callQuizAPI(topic);
    if (!data || data.error) {
      throw new Error("Invalid data received from API");
    }
    this.quiz = new Quiz(data);

    // Hide loading clues
    this.ui.hideLoading();

    
    // Show first question
    this.ui.showQuizContainer()
    this.nextQuestion();

    // Display quiz data in text box
    this.ui.displayQuizData(this.quiz.questions);
  }

  nextQuestion() {
    // Get question from quiz
    const question = this.quiz.getCurrentQuestion();
    // Update UI elements
    this.ui.displayCurrentQuestion(question);
  }

  // TODO: check answer
}

const app = new App();
