
"""
- I noticed that the previous version works incorrectly. It seems the error description wasn't provided, but we can infer potential issues related to the threading or server starting process.
- I suspect the server might not have started correctly before the request was made. I am increasing the server start wait time to ensure it initializes successfully.
- Instead of blocking with time.sleep(), I'm using a more reliable approach to check if the server is running before proceeding with the request by opening the URL to confirm its availability.
"""

from fastapi import FastAPI
from threading import Thread
import uvicorn
import requests
import time
from urllib.error import URLError
from urllib.request import urlopen

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

    try:
        # Nested loops to process the JSON
        for level1_key, level1_value in data.items():
            for level2_key, level2_value in level1_value.items():
                for level3_key, level3_value in level2_value.items():
                    for level4_key, level4_value in level3_value.items():
                        for level5_key, level5_value in level4_value.items():
                            # Store data in the internal dictionary
                            internal_dict[
                                f"{level1_key}.{level2_key}.{level3_key}.{level4_key}.{level5_key}"
                            ] = level5_value
                            element_count += 1
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

    # Return the count of elements
    return {"element_count": element_count}


# Function to generate a complex nested JSON
def generate_nested_json(levels=5, elements_per_level=5):
    def create_level(depth):
        if depth == 0:
            return {f"key_{i}": f"value_{i}" for i in range(elements_per_level)}
        else:
            return {
                f"level_{depth}_key_{i}": create_level(depth - 1)
                for i in range(elements_per_level)
            }

    return create_level(levels - 1)


# Function to run the FastAPI server
def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")


# Start the server in a separate thread
server_thread = Thread(target=run_server, daemon=True)
server_thread.start()

# Check if the server is running before making a request
def is_server_running(url, timeout=3):
    while True:
        try:
            urlopen(url, timeout=timeout)
            return True
        except URLError:
            time.sleep(0.1)

# Allow some time for the server to start by checking its availability
url = "http://127.0.0.1:8000/process/"
if is_server_running(url):
    # Client sends complex JSON to the API
    try:
        nested_json = generate_nested_json()
        response = requests.post(url, json=nested_json)
        print("Response from server:", response.json())
    except Exception as e:
        print("Error:", e)

# Stop the server
print("Done.")
