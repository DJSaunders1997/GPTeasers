[![Deploy static content to Pages](https://github.com/DJSaunders1997/GPTeasers/actions/workflows/static.yml/badge.svg)](https://github.com/DJSaunders1997/GPTeasers/actions/workflows/static.yml)
[![Trigger auto deployment for gpteasers](https://github.com/DJSaunders1997/GPTeasers/actions/workflows/gpteasers-AutoDeployTrigger-f53ae13c-780c-4431-b28c-18728d5a7dd7.yml/badge.svg)](https://github.com/DJSaunders1997/GPTeasers/actions/workflows/gpteasers-AutoDeployTrigger-f53ae13c-780c-4431-b28c-18728d5a7dd7.yml)
[![CodeQL](https://github.com/DJSaunders1997/GPTeasers/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/DJSaunders1997/GPTeasers/actions/workflows/github-code-scanning/codeql)
# GPTeasers 🧠💡

Welcome to **GPTeasers** - where we tickle your brain with quizzes from the depths of GPT's knowledge! 🎓🤖

https://djsaunders1997.github.io/GPTeasers/


## Overview 🌐

GPTeasers is a webapp that generates quiz-style questions based on the topic you provide. Want to challenge yourself with "Roman History" or dive deep into "Quantum Physics"? We've got you covered! 📚✨

![GPTeasers frontpage with options for quiz topic, difficulty, and AI provider](.images/GPTeasers_frontpage.png)

![GPTeasers quiz page showing questions, answers, and generatred image](.images/GPTeasers_quiz.png)

## Features 🌟

- **Dynamic Quizzes** 📝: Enter a topic and get a quiz in seconds!
- **Instant Feedback** 💬: Know right away if you're a genius or if it's time to hit the books.
- **Mobile Friendly** 📱: Quiz yourself anytime, anywhere.
- **Hosted on GitHub Pages** 🚀: Fast, reliable, and free!

## How to Use 🛠️

1. **Visit the App** 🌍: Go to the [GPTeasers site](https://djsaunders1997.github.io/GPTeasers/).
2. **Enter a Topic** 🔍: Type in your desired topic in the search box.
3. **Start the Quiz** 🎉: Answer the questions and see how you fare!
4. **Share & Challenge Friends** 🤝: Think you did well? Share your results and challenge a friend!


# Architecture

![Architecture Diagram](./images/Architecture.drawio.png)

1. Web Browser (Client): The user accesses the static site hosted on GitHub Pages.
2. GitHub Pages (Static Site): The static site serves content to the client. When specific actions are taken on the site (pressing a Generate Quz button), a call is made to the Azure Functions Backend.
3. Azure Container Apps: Once triggered, the FastAPI containers communicates with the OpenAI API, sending requests and receiving responses.
4. OpenAI API: Processes the request and sends back a response.

## Docker Compose Setup for Local Testing

This project uses Docker Compose to run both the FastAPI backend and the frontend services locally.

### Services

- **fastapi_generate_quiz**:  
  The FastAPI backend that serves the GPTeasers API. This container is responsible for handling requests from the frontend and interacting with the OpenAI API to generate quizzes.

- **frontend**:  
  A static frontend application. Although the site is hosted on GitHub Pages, this container allows you to test it locally.

### Running Locally

1. **Set Environment Variables**  
   Ensure that the `OPENAI_API_KEY` is set in your environment or in a `.env` file at the project root:
   ```sh
   export OPENAI_API_KEY=your_openai_api_key_here
   ```
   or create a `.env` file with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. **Build and Run the Containers**  
   From the project root, run:
   ```sh
   docker-compose up --build
   ```
   This command builds both the backend and frontend images and starts the containers.

3. **Access the Services**  
   - **Backend API (FastAPI)**:  
     Access via [http://localhost:8000](http://localhost:8000)
   - **Frontend**:  
     Access via [http://localhost:8080](http://localhost:8080)

By following these steps, you can easily test both your backend API and your static frontend locally using Docker Compose.
