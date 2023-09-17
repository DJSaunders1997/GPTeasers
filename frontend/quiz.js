// simple class called Quiz that wraps around the JSON response quz data

class Quiz {
  // Example data:
  // [
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
  constructor(data) {
    this.questions = data;
    this.currentIndex = 0;
    this.score = 0;
    this.numQuestions = this.questions.length;
  }

  // Get the current question without moving to the next one
  getCurrentQuestion() {
    if (this.currentIndex < this.numQuestions) {
      return this.questions[this.currentIndex];
    } else {
      alert("Quiz over!");
      return null;
    }
  }

  // Move to the next question and return it
  nextQuestion() {
    this.currentIndex++;
    return this.getCurrentQuestion();
  }

  // Check if there are more questions in the quiz
  hasMoreQuestions() {
    return this.currentIndex < this.numQuestions - 1;
  }

  // TODO: Convert this to return bool, and handle UI in UI.js and app.js
  checkAnswer(selectedOption) {
    if (!selectedOption) {
      console.error("No option selected");
      return;
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
        (this.currentIndex + 1) + " / " + this.numQuestions +
        "\nScore: " +
        this.score;

      alert(returnMessage);
    } else {
      //TODO: Eventually move this UI to UI class
      const returnMessage =
        "Wrong!" +
        "\n\nThe Correct Answer is:" +
        currentQuestion.answer +
        "\nExplanation: " +
        currentQuestion.explanation +
        "\n" +
        currentQuestion.wikipedia +
        "\nQuestion: " +
        (this.currentIndex + 1) + " / " + this.numQuestions +
        "\nScore: " +
        this.score;

      alert(returnMessage);
    }
    if (this.hasMoreQuestions()) {
      this.nextQuestion();
    } else {
      alert(
        "Quiz Finished!" +
          "\nFinal Score:" +
          this.score +
          "/" +
          (this.currentIndex + 1)
      );
      location.reload(); // This will reload the page
    }
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
