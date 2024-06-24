from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import time

app = FastAPI()

def stream_data():
    for i in range(10):  # Example: stream numbers from 0 to 9
        yield f"data: {i}\n\n"
        time.sleep(1)  # Simulate delay

@app.get("/stream")
async def stream():
    return StreamingResponse(stream_data(), media_type="text/event-stream")


# Run with uvicorn fast_test_streaming:app --reload
# Access with curl http://localhost:8000/stream
# This simple example works!