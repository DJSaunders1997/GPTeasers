# Backend API

This directory contains the FastAPI app that serves as the backend for the GPTeasers project.

### Note this used to use Azure Functions
- **Note**: This function uses FastAPI to address issues related to streaming, as discussed [here](https://github.com/Azure/azure-functions-python-worker/discussions/1349#discussioncomment-9777250).
- THIS IS CURRENTLY BLOCKED DUE TO NOT BEING ABLE TO INSTALL VERSION 4.31.0 on my laptop reee https://techcommunity.microsoft.com/t5/azure-compute-blog/azure-functions-support-for-http-streams-in-python-is-now-in/ba-p/4146697

## Structure

There is a single FastAPI web app defined that handles both AI aspects of the project:

### GenerateQuiz

Used to generate a quiz from a given topic using ChatGPT.
- **Note**: This function uses FastAPI to address issues related to streaming, as discussed [here](https://github.com/Azure/azure-functions-python-worker/discussions/1349#discussioncomment-9777250).
- THIS IS CURRENTLY BLOCKED DUE TO NOT BEING ABLE TO INSTALL VERSION 4.31.0 on my laptop reee https://techcommunity.microsoft.com/t5/azure-compute-blog/azure-functions-support-for-http-streams-in-python-is-now-in/ba-p/4146697

### GenerateImage

Used to generate an image from a prompt, using Dalle2.
- **Note**: This function utilizes plain Azure Functions without FastAPI.

Within each of these directories, there is a Python module to call the OpenAI API using my API key set as an Environment Variable, and both a Python module and a function.json that defines the Azure Function behavior.

## Deployment

Deployment is managed via GitHub Actions, which automatically builds and deploys the container to my Azure Container App.

## Environment Variables

Certain functions may require environment variables (e.g., `OPENAI_API_KEY`). These can be set in the Azure Portal under the Application Settings for the Function App.

## Debug 
To debug locally, follow these steps:

1. **Build the Docker container**:
    ```sh
    docker build -t fastapi_generate_quiz:latest .
    ```

2. **Run the Docker container**:
    ```sh
    docker run -p 8000:8000 -e OPENAI_API_KEY fastapi_generate_quiz:latest
    ```

3. **Test the endpoints using Postman or cURL**:

    ### GenerateQuiz
    ```sh
    curl "http://localhost:8000/GenerateQuiz?topic=UK%20History&difficulty=easy&n_questions=3"
    ```

    ### GenerateImage
    ```sh
    curl "http://localhost:8000/GenerateImage?prompt=Kangeroo%20Playing%20BasketBall"
    ```

4. **Tag the Docker image for GitHub Container Registry**:
    ```sh
    docker tag fastapi_generate_quiz:latest ghcr.io/djsaunders1997/fastapi_generate_quiz:latest
    ```

5. **Push the Docker image to GitHub Container Registry**:
    ```sh
    docker push ghcr.io/djsaunders1997/fastapi_generate_quiz:latest
    ```

## Running Tests

Our test suite is divided into **unit tests** and **integration tests**.

- **Unit Tests:**  
  These tests use mocks to simulate API responses. They run quickly and do not require real API calls.

- **Integration Tests:**  
  These tests make real API calls (e.g., to the OpenAI API) and require a valid API key. They are intended to be run manually or in a staging environment.

### Default Behavior

By default, integration tests are **excluded** from the test run. This is achieved by configuring `pytest` in our `pytest.ini` file (located in the `backend` directory):

```ini
[pytest]
markers =
    integration: mark test as an integration test.
addopts = -m "not integration"
```

This configuration tells `pytest` to skip any test marked with `@pytest.mark.integration` when you run:

```bash
pytest -v
```

### Running Integration Tests

To run the integration tests, override the default marker filter by using the `-m` option:

```bash
pytest -m integration
```

> **Note:** Integration tests make real API calls and require the `OPENAI_API_KEY` environment variable to be set. Make sure you have this environment variable configured before running these tests.

---
