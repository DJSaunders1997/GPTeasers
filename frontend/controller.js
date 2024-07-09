class Controller {
  constructor() {
    this.eventSource = null;
    this.messageCount = 0;
    this.messageCountLimit = 10;
    this.baseURLQuiz = "https://generate-quiz.nicehill-697d18fb.ukwest.azurecontainerapps.io/GenerateQuiz"
    this.baseURLImage = "https://gpteasers-generatequiz.azurewebsites.net/api/GenerateImage"
    this.quizData = []; // List to store the received quiz data
  }

  /**
   * Calls the Quiz API to fetch a quiz based on the provided topic.
   * Uses Server-Sent Events (SSE) to receive data in real-time.
   *
   * @param {string} topic - The topic for which the quiz is generated.
   * @param {string} difficulty - The difficulty level of the quiz.
   * @returns {Promise<void>} - No return value.
   * @throws {Error} When the network response is not ok.
   */
  async callQuizAPI(topic, difficulty) {
    console.log("Generating quiz for topic:", topic);
    console.log("Generating quiz with difficulty:", difficulty);

    const encodedTopic = encodeURIComponent(topic);
    const encodedDifficulty = encodeURIComponent(difficulty);
    const url = `${this.baseURLQuiz}?topic=${encodedTopic}&difficulty=${encodedDifficulty}`; // Adjust if running locally
    console.log(`Connecting to SSE endpoint: ${url}`);

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

        // Handle the received data (e.g., update UI)
        // TODO: Implement your own logic to handle the received data

        // Close the EventSource connection after receiving 10 messages
        if (this.messageCount >= this.messageCountLimit) {
          this.stopEventSource();
        }
      };

      // Error handling for the EventSource
      this.eventSource.onerror = (error) => {
        console.error('EventSource encountered an error:', error);
        this.stopEventSource();
      };
    } catch (error) {
      console.error("Error occurred during the API call:", error);
      throw error;
    }
  }

  /**
   * Stops the EventSource and cleans up.
   * This is called after receiving 10 messages or when an error occurs.
   */
  stopEventSource() {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
      console.log('EventSource connection closed after receiving 10 messages.');
    }
  }

  /**
   * Calls the Image Generation API to fetch an image based on the provided prompt.
   *
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

export default Controller;

// Example usage:
// c = new Controller;
// res = c.callImageAPI("Kangeroos")
// console.log(res)
// controller.callQuizAPI('Kangeroos', 'easy');