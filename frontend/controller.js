import fetch from 'node-fetch';
import EventSource from 'eventsource';

class Controller {
  // Public fields
  constructor() {
    this.eventSource = null;
    this.messageCount = 0;
    this.messageCountLimit = 2;
    this.baseURLQuiz = "https://generate-quiz.nicehill-697d18fb.ukwest.azurecontainerapps.io/GenerateQuiz";
    this.baseURLImage = "https://gpteasers-generatequiz.azurewebsites.net/api/GenerateImage";
    this.quizData = []; // List to store the received quiz data
  }

  /**
   * Calls the Quiz API to fetch a quiz based on the provided topic.
   * Uses Server-Sent Events (SSE) to receive data in real-time.
   *
   * @public
   * @param {string} topic - The topic for which the quiz is generated.
   * @param {string} difficulty - The difficulty level of the quiz.
   * @returns {Promise<Object[]>} The list of quiz data.
   * @throws {Error} When the network response is not ok.
   */
  callQuizAPI(topic, difficulty) {
    console.log("Generating quiz for topic:", topic);
    console.log("Generating quiz with difficulty:", difficulty);

    const encodedTopic = encodeURIComponent(topic);
    const encodedDifficulty = encodeURIComponent(difficulty);
    const url = `${this.baseURLQuiz}?topic=${encodedTopic}&difficulty=${encodedDifficulty}`;
    console.log(`Connecting to SSE endpoint: ${url}`);

    // Promises are used to handle asynchronous operations. They represent a value that may be available now, 
    // or in the future, or never. A promise is in one of these states:
    // - pending: initial state, neither fulfilled nor rejected.
    // - fulfilled: meaning that the operation completed successfully.
    // - rejected: meaning that the operation failed.

    // Here, we return a new promise that will resolve with the quizData once we have received 10 messages from the server.
    return new Promise((resolve, reject) => {
      try {
        // Initialize the EventSource to establish a connection to the server
        this.eventSource = new EventSource(url);
        this.messageCount = 0;

        // Event listener for messages received from the server
        this.eventSource.onmessage = (event) => {
          this.messageCount++;
          const data = JSON.parse(event.data);
          console.log(`Received message ${this.messageCount}:`, data);

          // Store the received data in the quizData list
          this.quizData.push(data);

          // Close the EventSource connection after receiving x messages
          if (this.messageCount >= this.messageCountLimit) {
            this.#stopEventSource();
            resolve(this.quizData); // Resolve the promise with the quizData
          }
        };

        // Error handling for the EventSource
        this.eventSource.onerror = (error) => {
          console.error('EventSource encountered an error:', error);
          this.#stopEventSource();
          reject(error); // Reject the promise if there's an error
        };
      } catch (error) {
        console.error("Error occurred during the API call:", error);
        reject(error); // Reject the promise if there's an error in the try block
      }
    });
  }

  /**
   * Stops the EventSource and cleans up.
   * This is called after receiving 10 messages or when an error occurs.
   *
   * @private
   */
  #stopEventSource() {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
      console.log(`EventSource connection closed after error or receiving ${this.messageCountLimit} messages.`);
    }
  }

  /**
   * Calls the Image Generation API to fetch an image based on the provided prompt.
   *
   * @public
   * @param {string} prompt - The prompt for which the image is generated.
   * @returns {Promise<Object>} The JSON response from the API containing image information.
   * @throws {Error} When the network response is not ok.
   */
  async callImageAPI(prompt) {
    console.log("Generating image for prompt:", prompt);

    const encodedPrompt = encodeURIComponent(prompt + " Pixel art");
    const url = `${this.baseURLImage}?code=&prompt=${encodedPrompt}`;
    console.log(`Sending request to: ${url}`);

    try {
      const response = await fetch(url);

      if (!response.ok) {
        console.error("Received a non-200 status code:", response.status);
        throw new Error("Network response was not ok");
      }

      const data = await response.text();
      console.log("Received data:", data);

      return data;
    } catch (error) {
      console.error("Error occurred during the API call:", error);
      throw error;
    }
  }
}

// export default Controller;

// Example usage
// var c = new Controller;
// var res = c.callImageAPI("Kangeroos");
// console.log(res);

// // Using promises to handle the asynchronous operation of fetching quiz data
// const c = new Controller();
// c.callQuizAPI('Kangeroos', 'easy')
//   .then(res => {
//     console.log('Quiz Data:', res); // This will log the quiz data after receiving the specified number of messages
//   })
//   .catch(err => {
//     console.error('Error:', err); // This will log any errors that occur during the process
//   });
