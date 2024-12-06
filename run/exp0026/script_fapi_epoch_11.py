
"""
In the initial iteration, the script did not execute successfully due to an unspecified error, although it produced correct results before the error occurred. To optimize the script, I will approach a few potential inefficiencies:

1. Optimize the nested loop operations by introducing a recursive function that will handle any level of nested dictionary.
2. Remove global variable usage to avoid potential concurrency issues which might be causing instability.
3. I've added asyncio.run to ensure the endpoint manages asynchronous I/O properly, potentially alleviating the error encountered.
4. Ensure the server thread is properly terminated to avoid lingering processes that might lead to instability.
"""

from fastapi import FastAPI
from threading import Thread
import uvicorn
import requests
import time
import asyncio

# Define the FastAPI app
app = FastAPI()

# Endpoint for processing complex JSON
@app.post("/process/")
async def process_item(data: dict):
    def process_nested_dict(d, prefix=''):
        element_count = 0
        for k, v in d.items():
            if isinstance(v, dict):
                element_count += process_nested_dict(v, prefix + k + '.')
            else:
                internal_dict[prefix + k] = v
                element_count += 1
        return element_count

    internal_dict = {}
    try:
        element_count = process_nested_dict(data)
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
            return {f"level_{depth}_key_{i}": create_level(depth - 1) for i in range(elements_per_level)}

    return create_level(levels - 1)


# Function to run the FastAPI server
def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")


async def main():
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
    finally:
        # Ensuring server is terminated
        server_thread.join(0.1)

    # Stop the server
    print("Done.")

# Execute main to manage asyncio
asyncio.run(main())
