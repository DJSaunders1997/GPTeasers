[![Deploy static content to Pages](https://github.com/DJSaunders1997/GPTeasers/actions/workflows/static.yml/badge.svg)](https://github.com/DJSaunders1997/GPTeasers/actions/workflows/static.yml)
[![Trigger auto deployment for gpteasers](https://github.com/DJSaunders1997/GPTeasers/actions/workflows/gpteasers-AutoDeployTrigger-f53ae13c-780c-4431-b28c-18728d5a7dd7.yml/badge.svg)](https://github.com/DJSaunders1997/GPTeasers/actions/workflows/gpteasers-AutoDeployTrigger-f53ae13c-780c-4431-b28c-18728d5a7dd7.yml)
[![CodeQL](https://github.com/DJSaunders1997/GPTeasers/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/DJSaunders1997/GPTeasers/actions/workflows/github-code-scanning/codeql)
# GPTeasers 🧠💡

Welcome to GPTeasers – a quiz app that challenges your brain with dynamically generated questions. Whether you’re into Roman History or Quantum Physics, GPTeasers has you covered. We even let you choose from multiple AI providers, so you can experience different styles of quiz generation.

https://djsaunders1997.github.io/GPTeasers/

## Overview

GPTeasers is a straightforward web app that creates quiz-style questions based on topics you select. Simply enter a subject you’re curious about, and our system will generate a quiz just for you using advanced AI. With support for multiple AI providers.

### Front Page
![GPTeasers frontpage with options for quiz topic, difficulty, and AI provider](images/GPTeasers_frontpage.png)

### Quiz Page
![GPTeasers quiz page showing questions, answers, and generated image](images/GPTeasers_quiz.png)

## Features

- **Dynamic Quizzes**: Input any topic and receive a quiz in seconds using genAI.
- **Multiple AI Providers**: Select from a range of AI services to get different quiz styles.
- **Hosted on GitHub Pages**: Fast, reliable, and free.

## How to Use

1. **Visit the App**: Go to the [GPTeasers site](https://djsaunders1997.github.io/GPTeasers/).
2. **Enter a Topic**: Type in your desired topic.
3. **Start the Quiz**: Answer the questions and see your results.
4. **Share & Challenge Friends**: Think you aced it? Share your score and challenge your friends!

# Architecture

![Architecture Diagram](./images/Architecture.drawio.png)

1. **Web Browser (Client)**: The user interact with a static site hosted on GitHub Pages.
2. **GitHub Pages (Static Site)**: Delivers the site’s content. When you hit “Generate Quiz”, the site communicates with our backend.
3. **Azure Container Apps**: The FastAPI backend processes your quiz request and works with different AI providers.
4. **AI Providers**: Multiple AI services process your input and generate unique quiz questions.

## Docker Compose Setup for Local Testing

This project uses Docker Compose to run both the FastAPI backend and the frontend services locally.

### Services

- **fastapi_generate_quiz**:  
  The FastAPI backend handles quiz generation by interacting with various AI providers.

- **frontend**:  
  A static version of the front end for local testing (even though the production site is on GitHub Pages).

### Running Locally

1. **Set Environment Variables**  
   Make sure your `OPENAI_API_KEY` is set in your environment or in a `.env` file at the project root:
   ```sh
   export OPENAI_API_KEY=your_openai_api_key_here
   ```
   Or create a `.env` file with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. **Build and Run the Containers**  
   From the project root, run:
   ```sh
   docker-compose up --build
   ```
   This command builds and starts both the backend and frontend containers.

3. **Access the Services**  
   - **Backend API (FastAPI)**: [http://localhost:8000](http://localhost:8000)
   - **Frontend**: [http://localhost:8080](http://localhost:8080)

With these steps, you can easily test both the backend API and the static frontend locally using Docker Compose.

