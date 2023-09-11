/**
 * This file contains functions related to the GPTeasers Quiz App.
 * It manages the fetching of quiz data from the API and its presentation on the web page.
 */

/**
 * Calls the Quiz API to fetch a quiz based on the provided topic.
 *
 * @param {string} topic - The topic for which the quiz is generated.
 * @returns {Promise<Object>} The JSON response from the API containing quiz information.
 * @throws {Error} When the network response is not ok.
 */
async function callQuizAPI(topic) {
  console.log("Generating quiz for topic:", topic);

  const url = `https://gpteasers-generatequiz.azurewebsites.net/api/GenerateQuiz?topic=${topic}`;
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
 * Generates and displays a quiz based on the topic provided by the user.
 * It fetches quiz data from the API, parses it, and then updates the DOM.
 *
 * @async
 * @function
 * @throws {Error} Throws an error if there's an issue generating the quiz.
 */

async function generateQuiz() {
  let topic = document.getElementById("quizTopic").value;

  try {
    const data = await callQuizAPI(topic);

    // Parse the data and display it
    let output = data.choices[0].text.trim();

    // Split question and options for simplicity (Assuming a specific format)
    let parts = output.split("\n");
    let question = parts[0];
    let options = parts.slice(1);

    document.getElementById("questionText").innerText = question;

    let optionsHtml = options
      .map((option, index) => {
        let label = String.fromCharCode(65 + index); // Convert 0 to A, 1 to B, etc.
        return `<label><input type="radio" name="answerOption" value="${label}"> ${option}</label><br>`;
      })
      .join("");

    document.getElementById("answerOptions").innerHTML = optionsHtml;

    document.getElementById("inputContainer").style.display = "none";
    document.getElementById("questionContainer").style.display = "block";
  } catch (error) {
    console.error("Error generating quiz:", error);
  }
}

/**
 * Handles the answer submission logic.
 * Currently, it just alerts that the answer has been submitted.
 */
function checkAnswer() {
  // In a real app, you'd check the answer using your backend or the API. This is just a prototype.
  alert("Answer submitted!");
}

// Test API Call
//   callQuizAPI("Kangeroos");
