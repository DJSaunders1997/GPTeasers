from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def stream_data():
    for i in range(100):  # Example: stream numbers from 0 to 9
        yield f"data: {i}\n\n"
        time.sleep(1)  # Simulate delay

@app.get("/stream")
async def stream():
    return StreamingResponse(stream_data(), media_type="text/event-stream")


# Run with uvicorn fast_test_streaming:app --reload --log-level debug
# Access with curl http://localhost:8000/stream
# This simple example works!