class Game {
    constructor(ui) {
        this.ui = ui;  // We're injecting the UI class into our game so that we can manipulate UI based on game logic.
        this.score = 0
        this.correctAnswers = 0
    }

    setData(quizData) {
        console.log("to implement")

        // TODO: Parse quiz into array of questions

    }

    async fetchQuizData() {
        this.ui.showLoading();

        try {
            const data = await callQuizAPI(this.ui.topicInput.value);
            this.ui.displayQuizData(data);
        } catch (error) {
            console.error("API Call Error:", error);
            alert("An error occurred. Please check the console for more details.");
        } finally {
            this.ui.hideLoading();
        }
    }

    // ... You can add more game-related methods, like checkAnswer, calculateScore, etc.
}

export default Game;