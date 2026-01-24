/**
 * Configuration constants for DOM selectors and CSS classes.
 * Centralizes all hardcoded strings for easier maintenance.
 */

export const HTML_ELEMENT_IDS = {
  // Quiz generation
  fetchQuizButton: "#fetchQuizButton",
  quizTopic: "#quizTopic",
  quizDifficulty: "#quizDifficulty",
  quizModel: "#quizModel",

  // Quiz interaction
  optionA: "#option-A",
  optionB: "#option-B",
  optionC: "#option-C",
  nextQuestionButton: "#nextQuestionButton",
  newQuizButton: "#newQuizButton",

  // History
  historySection: "#quizHistory",
  historyList: "#quizHistoryList",
  historyEmptyMessage: "#historyEmptyMessage",

  // UI containers
  inputContainer: "#inputContainer",
  intro: "#intro",
  quizContainer: "#quiz-container",
  quizSection: "#quizSection",

  // Quiz display elements
  quizTitle: "#quizTitle",
  quizProgress: "#quizProgress",
  quizScore: "#quizScore",
  questionText: "#question-text",
  quizFeedback: "#quizFeedback",
  AIImage: "#AIImage",

  // Loading elements
  loadingMessage: "#loadingMessage",
  loadingBarContainer: "#loadingBarContainer",
  loadingBar: "#loadingBar",

  // Navigation
  navbarToggle: "#navbar-toggle",
  navbarLinks: "#navbar-links",
};

export const CSS_CLASSES = {
  quizMeta: "quiz-meta",
  quizFeedback: "quiz-feedback",
  feedbackCorrect: "feedback-correct",
  feedbackWrong: "feedback-wrong",
  feedbackFinal: "feedback-final",
  feedbackChoices: "feedback-choices",
  choiceCorrect: "choice-correct",
  choiceNeutral: "choice-neutral",
  navbarActive: "active",
};

/**
 * Safely retrieve a DOM element by its selector.
 * @param {string} selector - ID selector (e.g., "#elementId")
 * @returns {HTMLElement|null} The element or null if not found
 */
export function getElement(selector) {
  // Remove # if present and use getElementById for performance
  const id = selector.startsWith("#") ? selector.slice(1) : selector;
  return document.getElementById(id);
}
