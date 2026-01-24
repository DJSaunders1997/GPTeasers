/**
 * DOMElements class manages and caches references to all DOM elements used by the UI.
 * Keeps element selection logic separate from UI behavior.
 */

import { HTML_ELEMENT_IDS, getElement } from "./config.js";

class DOMElements {
  constructor() {
    // Input/Form elements
    this.inputContainer = getElement(HTML_ELEMENT_IDS.inputContainer);
    this.intro = getElement(HTML_ELEMENT_IDS.intro);
    this.topicInput = getElement(HTML_ELEMENT_IDS.quizTopic);
    this.quizDifficulty = getElement(HTML_ELEMENT_IDS.quizDifficulty);
    this.quizModel = getElement(HTML_ELEMENT_IDS.quizModel);
    this.fetchButton = document.querySelector("button"); // First button on page

    // Image element
    this.AIImage = getElement(HTML_ELEMENT_IDS.AIImage);

    // Quiz container and display
    this.quizContainer = getElement(HTML_ELEMENT_IDS.quizContainer);
    this.quizTitle = getElement(HTML_ELEMENT_IDS.quizTitle);
    this.quizProgress = getElement(HTML_ELEMENT_IDS.quizProgress);
    this.quizScore = getElement(HTML_ELEMENT_IDS.quizScore);
    this.questionText = getElement(HTML_ELEMENT_IDS.questionText);
    this.quizFeedback = getElement(HTML_ELEMENT_IDS.quizFeedback);

    // Answer buttons
    this.buttonA = getElement(HTML_ELEMENT_IDS.optionA);
    this.buttonB = getElement(HTML_ELEMENT_IDS.optionB);
    this.buttonC = getElement(HTML_ELEMENT_IDS.optionC);
    this.nextQuestionButton = getElement(HTML_ELEMENT_IDS.nextQuestionButton);

    // Loading indicators
    this.loadingMessage = getElement(HTML_ELEMENT_IDS.loadingMessage);
    this.loadingBarContainer = getElement(HTML_ELEMENT_IDS.loadingBarContainer);
    this.loadingBar = getElement(HTML_ELEMENT_IDS.loadingBar);
  }

  /**
   * Get all answer buttons as an array.
   * @returns {HTMLElement[]} Array of answer option buttons
   */
  getAnswerButtons() {
    return [this.buttonA, this.buttonB, this.buttonC];
  }
}

export default DOMElements;
