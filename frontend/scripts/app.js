/**
 * This file contains functions related to the GPTeasers Quiz App.
 * It manages the fetching of quiz data from the API and its presentation on the web page.
 */
import Controller from "./controller.js";
import UI from "./ui.js";
import Quiz from "./quiz.js";

class App {
  constructor() {
    const numQuestions = 10;
    // Initialise app elements as JS objects.
    this.quiz = new Quiz(numQuestions);
    this.controller = new Controller(this.quiz);
    this.ui = new UI();

    // Initialise button event listeners.
    // The arrow function implicitly binds the method to the current instance of this class.
    document
      .querySelector("#fetchQuizButton")
      .addEventListener("click", () => this.fetchQuizData());
    document
      .querySelector("#fetchQuizButton")
      .addEventListener("click", () => this.fetchAIImage());
    // Answer buttons aren't visible when the page first loads
    document
      .querySelector("#option-A")
      .addEventListener("click", () => this.checkAnswer("A"));
    document
      .querySelector("#option-B")
      .addEventListener("click", () => this.checkAnswer("B"));
    document
      .querySelector("#option-C")
      .addEventListener("click", () => this.checkAnswer("C"));

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
    // Get the topic and difficulty from the input field
    const topic = this.ui.getTopic();
    const difficulty = this.ui.getDifficulty();

    // Check if topic is empty or contains only whitespace
    if (!topic.trim()) {
      alert("Please enter a valid topic.");
      return; // Exit the function early without further processing
    }

    // Show loading clues
    this.ui.showLoading();

    try {
      // Generate Quiz
      // The await keyword is used to wait for the asynchronous callQuizAPI method to complete.
      // This means the code execution will pause here until callQuizAPI returns a result or throws an error.
      // It's like telling JavaScript to wait here and don't move to the next line until this promise is resolved.
      // use the onQuestionReceived callback to display each question individually as it is added to the Quiz object.
      // Arrow function: Shorter syntax for functions and keeps 'this' context from surrounding code
      // TODO: Find out how this makes the app actually work?
      // TODO: I only want to wait for the first event to come in, then continue and let it the quiz populate in the background
      await this.controller.callQuizAPI(topic, difficulty, (question) => {
        console.log("Question received!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
        this.showQuestion(); // Question should've been added to quiz, so display it
        // This inner code runs each message. I want after only the first message!!!
        // TODO: Only run these on the first run?
        this.ui.hideLoading(); // Hide loading clues
        this.ui.showQuizContainer(topic); // Show quiz container
      });
      console.log("Just Exited AWAIT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
    } catch (error) {
      console.error("Error fetching quiz data:", error);
      alert("Failed to fetch quiz data. Please try again.");
      this.ui.hideLoading();
    }
  }

  async fetchAIImage() {
    // Use the topic as a prompt to image
    const prompt = document.getElementById("quizTopic").value;

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
  }

  // Calls quiz check answer method
  // and displays the next question
  checkAnswer(answer) {
    this.quiz.checkAnswer(answer);
    this.showQuestion();
  }
}

const app = new App();
