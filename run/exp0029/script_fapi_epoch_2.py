
# In the previous version of code we had complex structure of generating data and internal structure of the application. We can simplify both of them to reduce the execution time.

from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread
import uvicorn
import requests
import time
import itertools

# Define the FastAPI app
app = FastAPI()

# Global element count
element_count = 0

# Endpoint for processing complex JSON
@app.post("/process/")
async def process_item(data: dict):

    # Reset element count
    global element_count
    element_count = 0
    data = list(itertools.chain.from_iterable(data.values()))
    element_count = len(data)

    # Return the count of elements
    return {"element_count": element_count}


# Function to generate a complex nested JSON
def generate_nested_json(levels=5, elements_per_level=5):
    return [str(i) for i in range(elements_per_level**levels)]

# Function to run the FastAPI server
def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

# Start the server in a separate thread
server_thread = Thread(target=run_server, daemon=True)
server_thread.start()

# Allow some time for the server to start
time.sleep(1)

# Client sends complex JSON to the API
try:
    url = "http://127.0.0.1:8000/process/"
    nested_json = generate_nested_json()
    response = requests.post(url, json=nested_json)
    print("Response from server:", response.json())
except Exception as e:
    print("Error:", e)

# Stop the server
print("Done.")
