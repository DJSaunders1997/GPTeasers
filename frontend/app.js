/**
 * This file contains functions related to the GPTeasers Quiz App.
 * It manages the fetching of quiz data from the API and its presentation on the web page.
 */
import Controller from './controller.js';
import Game from './game.js';
import UI from './ui.js';

class App {
  constructor() {
    // Initialise app elements as JS objects.
    this.controller = new Controller();
    this.ui = new UI();
    this.game = new Game(this.ui);

    // Initialise button event listener.
    // The arrow function implicitly binds the method to the current instance of this class.
    document.querySelector('#fetchQuizButton').addEventListener('click', () => this.fetchQuizData());
  }

  async fetchQuizData() {
  
    // Get the topic from the input field
    const topic = document.getElementById('quizTopic').value;

    // Check if topic is empty or contains only whitespace
    if (!topic.trim()) {
      alert("Please enter a valid topic.");
      return;  // Exit the function early without further processing
    }

    // Show loading clues
    this.ui.showLoading();

    // Generate Quiz
    const data = await this.controller.callQuizAPI(topic);
    document.getElementById('jsonResponse').textContent = JSON.stringify(data, null, 2);

    // Hide loading clues
    this.ui.hideLoading();

    // Display quiz data in text box
    this.ui.displayQuizData(data);
  }
}

const app = new App();
