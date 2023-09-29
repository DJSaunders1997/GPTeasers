# Frontend Drectory

This app is a single static HTML webpage hosted with github pages.
The .js files control dynamic logic, and calling the backend.

## Directory Structure

```
.
├── app.js              # Main application logic
├── controller.js       # Backend API interaction
├── quiz.js             # Quiz related logic
├── index.html          # Main HTML page for the
├── loadingbar.js       # Loading bar animation
└── ui.js               # User Interface related
```

## File Descriptions

### `app.js`

This file contains the main logic for the GPTeasers Quiz App. 
It manages the fetching of quiz data from the API and its presentation on the web page. 
It also handles user interactions, such as clicking the "Fetch Quiz Data" button and input validation.

### `controller.js`

This class is responsible for interacting with the backend API. 
It contains methods to call the Quiz API based on a given topic and processes the API response.

### `quiz.js`

The Quiz class contains methods related to quiz logic, 
such as parsing quiz data, checking answers, calculating scores, etc.

### `index.html`

The main HTML page for the GPTeasers Quiz App. 
This page provides a UI for users to input a quiz topic, fetch quiz data, and interact with the fetched quiz.

### `loadingbar.js`

This class represents a loading bar. 
It provides methods to start and stop a loading bar animation, which gives users feedback during longer operations.

### `ui.js`

The UI class provides methods related to the user interface. 
It contains methods to show/hide loading animations, 
display fetched quiz data on the web page, and manipulate other UI elements based on user interactions and quiz logic.

## Setup and Usage

1. Open `index.html` in a modern web browser.
2. Enter a quiz topic in the provided input field.
3. Click the "Fetch Quiz Data" button.
4. The app will fetch quiz data related to the given topic and display it on the page.
