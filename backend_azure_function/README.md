# Backend Azure Functions

This directory contains the Azure Functions that serve as the backend for the GPTeasers project. Each function is dedicated to a specific task within the system, allowing for modularity and easy maintenance.

## Structure

There are 2 Azure Functions defined n the backend_azure_function app:

### GenerateQuiz

Used to generate a quiz from a given topic using ChatGPT.

### GenerateImage

Used to generate an image from a prompt, using Dalle2.


Within each of these directories there is a python module to call the OpenAI API using my API key set as an Environment Variable, and both a python module and a function.json that defines the Azure Function behavior.


## Deployment

Deployment is managed via GitHub Actions, which automatically builds and deploys the functions to Azure upon code pushes to the repository. Ensure you've linked your Azure account and set up the necessary secrets in your GitHub repository.

## Environment Variables

Certain functions may require environment variables (e.g., `OPENAI_API_KEY`). These can be set in the Azure Portal under the Application Settings for the Function App.

## Debug 
To debug locally first install [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=linux%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python).

Ensure you are in the azure_functions directory: `cd backend_azure_function`

Run the functions locally with `func run`

Test these using PostMan or these cURl's:
### GenerateQuiz

`curl 'http://localhost:7071/api/GenerateQuiz?topic=UK%20History'`

### GenerateImage


`curl 'http://localhost:7071/api/GenerateImage?prompt=Kangeroo%20Playing%20BasketBall'`