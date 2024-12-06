
"""
I noticed that the previous version works incorrectly. I analysed the issue and fixed it. Also I understand that I shouldn’t take to account execution time of not working version.
To optimize the current implementation, I will avoid re-running the server for each request as it seems redundant and time-consuming. The server should ideally run independently and process requests continuously. I'll structure the code to demonstrate this by creating a main entry point that initializes and processes through requests without stopping and restarting the server. 

Other optimizations I intend to implement:
1. Using `httpx` library instead of `requests` to handle asynchronous requests more efficiently.
2. Utilizing the latest features and best practices of FastAPI and uvicorn.
3. Avoiding global variables where possible and using context management to keep the code cleaner.
"""

from fastapi import FastAPI
from threading import Thread
import uvicorn
import httpx
import asyncio

# Define the FastAPI app
app = FastAPI()

# Endpoint for processing complex JSON
@app.post("/process/")
async def process_item(data: dict):
    internal_dict = {}
    element_count = 0

    try:
        # Nested loops to process the JSON
        for level1_key, level1_value in data.items():
            for level2_key, level2_value in level1_value.items():
                for level3_key, level3_value in level2_value.items():
                    for level4_key, level4_value in level3_value.items():
                        for level5_key, level5_value in level4_value.items():
                            # Store data in the internal dictionary
                            internal_dict[f"{level1_key}.{level2_key}.{level3_key}.{level4_key}.{level5_key}"] = level5_value
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
            return {f"level_{depth}_key_{i}": create_level(depth - 1) for i in range(elements_per_level)}

    return create_level(levels - 1)


# Function to run the FastAPI server
def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")


# Using asyncio and httpx to handle requests
async def make_request():
    async with httpx.AsyncClient() as client:
        try:
            url = "http://127.0.0.1:8000/process/"
            nested_json = generate_nested_json()
            response = await client.post(url, json=nested_json)
            print("Response from server:", response.json())
        except Exception as e:
            print("Error:", e)


# Start the server in a separate thread
server_thread = Thread(target=run_server, daemon=True)
server_thread.start()

# Allow some time for the server to start
await asyncio.sleep(1)

# Client sends complex JSON to the API
await make_request()

# Since the server is running in a daemon thread, we do not explicitly stop it here.
print("Done.")
