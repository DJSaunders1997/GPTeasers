# FastAPI Example from Docker docs 
# https://fastapi.tiangolo.com/deployment/docker/#dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /code

# Copy requirements file and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application code
COPY . /code

# Command to run the application using Uvicorn
CMD ["uvicorn", "fastapi_generate_quiz:app", "--host", "0.0.0.0", "--port", "8000"]

# docker build -t fastapi_generate_quiz:latest .        # Build container
# docker run -p 8000:8000 -e OPENAI_API_KEY fastapi_generate_quiz:latest        # Run container
# curl "http://localhost:8000/GenerateQuiz?topic=UK%20History&difficulty=easy&n_questions=3"      # CURL container in another terminal to test quiz
# curl "http://localhost:8000/GenerateImage?prompt=A%20Juicy%20Burger"      # CURL container in another terminal to test image
# docker tag fastapi_generate_quiz:latest ghcr.io/djsaunders1997/fastapi_generate_quiz:latest       # Tag this container in github registry format 
# docker push ghcr.io/djsaunders1997/fastapi_generate_quiz:latest       # Push to github container registry
