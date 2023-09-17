// Class to interact with backend api
class Controller {
  constructor() {}

  /**
   * Calls the Quiz API to fetch a quiz based on the provided topic.
   *
   * @param {string} topic - The topic for which the quiz is generated.
   * @returns {Promise<Object>} The JSON response from the API containing quiz information.
   * @throws {Error} When the network response is not ok.
   */
  async callQuizAPI(topic, difficulty) {
    console.log("Generating quiz for topic:", topic);
    console.log("Generating quiz with difficulty:", difficulty);

    const encodedTopic = encodeURIComponent(topic);
    const encodedDifficulty = encodeURIComponent(topic);
    const url = `https://gpteasers-generatequiz.azurewebsites.net/api/GenerateQuiz?topic=${encodedTopic}&difficulty=${difficulty}`;
    console.log(`Sending request to: ${url}`);

    try {
      const response = await fetch(url);

      if (!response.ok) {
        console.error("Received a non-200 status code:", response.status);
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      console.log("Received data:", data);

      return data;
    } catch (error) {
      console.error("Error occurred during the API call:", error);
      throw error;
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
    const url = `https://gpteasers-generatequiz.azurewebsites.net/api/GenerateImage?code=&prompt=${encodedPrompt}`;
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

// c = new Controller;
// res = c.callImageAPI("Kangeroos")

// console.log(typeof(res))
// console.log(res)