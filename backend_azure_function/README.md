# Backend Azure Functions

This directory contains the Azure Functions that serve as the backend for the GPTeasers project.

## Structure

There are 2 Azure Functions defined n the backend_azure_function app:

### GenerateQuiz

Used to generate a quiz from a given topic using ChatGPT.
- **Note**: This function uses FastAPI to address issues related to streaming, as discussed [here](https://github.com/Azure/azure-functions-python-worker/discussions/1349#discussioncomment-9777250).


### GenerateImage

Used to generate an image from a prompt, using Dalle2.
- **Note**: This function utilizes plain Azure Functions without FastAPI.

Within each of these directories there is a python module to call the OpenAI API using my API key set as an Environment Variable, and both a python module and a function.json that defines the Azure Function behavior.


## Deployment

Deployment is managed via GitHub Actions, which automatically builds and deploys the functions to Azure upon specific triggers:
- **Production Deployment**: Code pushes to the `main` branch trigger deployments to the production slot.
- **Slot Deployment**: Tags starting with `slot` trigger deployments to a specific testing slot named `slot`. This allows for isolated testing before merging changes into production. See the docs [here](https://learn.microsoft.com/en-us/azure/azure-functions/functions-deployment-slots?tabs=azure-portal).


## Environment Variables

Certain functions may require environment variables (e.g., `OPENAI_API_KEY`). These can be set in the Azure Portal under the Application Settings for the Function App.

## Debug 
To debug locally first install [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=linux%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python).

Ensure you are in the azure_functions directory: `cd backend_azure_function`

Run the functions locally with `func start`

Test these using PostMan or these cURl's:
### GenerateQuiz

`curl 'http://localhost:7071/api/GenerateQuiz?topic=UK%20History'`

### GenerateImage


`curl 'http://localhost:7071/GenerateImage?prompt=Kangeroo%20Playing%20BasketBall'`