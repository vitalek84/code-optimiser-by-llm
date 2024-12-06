
"""
I noticed that the previous version works incorrectly. I analysed the issue, the execution time for the previous version is exactly the same as the base version
and the error description is empty, indicating a timeout or a silent failure. I'm going to focus on optimizing the nested loops and processing steps.
Since the internal processing is loop intensive, I aim to use concurrent execution to take advantage of multiple CPU cores.
Additionally, I'll adjust the server wait time and try to avoid blocking calls by using asyncio and HTTPX for asynchronous requests.
"""

from fastapi import FastAPI
from threading import Thread
import uvicorn
import asyncio
import httpx
import time

# Define the FastAPI app
app = FastAPI()

# Internal storage dictionary
internal_dict = {}

# Endpoint for processing complex JSON
@app.post("/process/")
async def process_item(data: dict):
    global internal_dict
    internal_dict = {}  # Reset internal dictionary
    element_count = 0

    # Flatten the nested JSON using async combinatoric traversal to avoid blocking
    async def process_level(prefix, level):
        nonlocal element_count
        if isinstance(level, dict):
            for key, value in level.items():
                await process_level(f"{prefix}.{key}", value)
        else:
            internal_dict[prefix] = level
            element_count += 1

    await process_level("", data)

    # Return the count of elements
    return {"element_count": element_count}


# Function to generate a complex nested JSON
def generate_nested_json(levels=5, elements_per_level=5):
    def create_level(depth):
        if depth == 0:
            return {f"key_{i}": f"value_{i}" for i in range(elements_per_level)}
        else:
            return {f"level_{depth}_key_{i}": create_level(depth - 1) for i in range(elements_per_level)}

    return create_level(levels - 1)


# Function to run the FastAPI server
def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")


# Start the server in a separate thread
server_thread = Thread(target=run_server, daemon=True)
server_thread.start()

# Allow some time for the server to start
time.sleep(1)

# Asynchronous client to send complex JSON to the API
async def send_request():
    url = "http://127.0.0.1:8000/process/"
    nested_json = generate_nested_json()
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=nested_json)
        print("Response from server:", response.json())

# Run the asynchronous request
asyncio.run(send_request())

# Stop the server
print("Done.")
