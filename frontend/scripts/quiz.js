// simple class called Quiz that wraps around the JSON response quz data

class Quiz {
  /**
   * Creates an instance of Quiz.
   * @param {int} numQuestions - Total number of questions in Quiz
   *
   * @constructor
   */
  constructor(numQuestions) {
    this.questions = [];
    this.currentIndex = 0;
    this.score = 0;
    this.numQuestions = numQuestions;
    this.numCurrentQuestions = this.questions.length;
  }

  /**
   * Adds a question to the quiz.
   *
   * @param {Object} question - The question object to add.
   */
  addQuestion(question) {
    this.questions.push(question);
    this.numCurrentQuestions = this.questions.length;
  }

  /**
   * Get the current question without moving to the next one.
   *
   * @returns {Object|null} The current question object or null if the quiz is over.
   */
  getCurrentQuestion() {
    console.log(
      "getCurrentQuestion called. Current index:",
      this.currentIndex,
      "Number of Quesitions:",
      this.numQuestions
    );

    if (this.currentIndex < this.numQuestions) {
      console.log("Current question:", this.questions[this.currentIndex]);
      return this.questions[this.currentIndex];
    } else {
      console.log("Quiz over!");
      alert("Quiz over!");
      return null;
    }
  }

  /**
   * Move to the next question and return it.
   *
   * @returns {Object|null} The next question object or null if the quiz is over.
   */
  nextQuestion() {
    this.currentIndex++;
    return this.getCurrentQuestion();
  }

  /**
   * Check if there are more questions in the quiz.
   *
   * @returns {boolean} True if there are more questions, false otherwise.
   */
  hasMoreQuestions() {
    return this.currentIndex < this.numQuestions - 1;
  }

  /**
   * Check the answer for the current question.
   *
   * @param {string} selectedOption - The selected answer option.
   * @returns {boolean} True if the answer is correct, false otherwise.
   */
  checkAnswer(selectedOption) {
    if (!selectedOption) {
      console.error("No option selected");
      return false;
    }
    const currentQuestion = this.getCurrentQuestion();

    if (selectedOption === currentQuestion.answer) {
      this.score++;
      const returnMessage =
        "Correct!" +
        "\n\nExplanation: " +
        currentQuestion.explanation +
        "\n" +
        currentQuestion.wikipedia +
        "\nQuestion: " +
        (this.currentIndex + 1) +
        " / " +
        this.numQuestions +
        "\nScore: " +
        this.score;

      alert(returnMessage);
      // return true;
    } else {
      const returnMessage =
        "Wrong!" +
        "\n\nThe Correct Answer is: " +
        currentQuestion.answer +
        "\nExplanation: " +
        currentQuestion.explanation +
        "\n" +
        currentQuestion.wikipedia +
        "\nQuestion: " +
        (this.currentIndex + 1) +
        " / " +
        this.numQuestions +
        "\nScore: " +
        this.score;

      alert(returnMessage);
      // return false;
    }
    if (this.hasMoreQuestions()) {
      this.nextQuestion();
    } else {
      this.endQuiz();
    }
  }

  /**
   * End the quiz and show the final score.
   */
  endQuiz() {
    alert(
      "Quiz Finished!" +
        "\nFinal Score: " +
        this.score +
        "/" +
        this.numQuestions
    );
    location.reload(); // This will reload the page
  }
}

// Sample usage:
// const quizData =  [
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
//     {
//         "question_id": 2,
//         "question": "Which breed of cat is known for its short legs?",
//         "A": "Persian",
//         "B": "Siamese",
//         "C": "Munchkin",
//         "answer": "C",
//         "explanation": "The breed of cat known for its short legs is the Munchkin.",
//         "wikipedia": "https://en.wikipedia.org/wiki/Munchkin_cat",
//         "dalle_prompt": "Image of a Munchkin cat"
//     }
// ]
// const quiz = new Quiz(quizData);

// console.log("Get the first question:")
// console.log(quiz.getCurrentQuestion()); // Get the first question
// console.log("Get A option:")
// console.log(quiz.getCurrentQuestion().A); // Get A option
// console.log("Get the next question:")
// console.log(quiz.nextQuestion());       // Move to the next question and get it
// console.log("See if more Questions are available")
// console.log(quiz.hasMoreQuestions());   // Check if more questions are available

export default Quiz;
