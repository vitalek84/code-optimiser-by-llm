
"""
Optimization Strategy:
1. Replace global dictionary with a local one to avoid the overhead of accessing shared mutable data.
2. Use more efficient data structures and algorithms if applicable.
3. Minimize I/O operations by handling server start-up and client requests more efficiently.
4. Utilize asynchronous programming for better performance in IO-bound tasks.

This version should have a significant reduction in execution time by minimizing global state access and improving the server/client interaction.
"""
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import requests
import asyncio

# Define the FastAPI app
app = FastAPI()

# Endpoint for processing complex JSON
@app.post("/process/")
async def process_item(data: dict):
    element_count = 0

    try:
        # Nested loops to process the JSON
        for level1_key, level1_value in data.items():
            for level2_key, level2_value in level1_value.items():
                for level3_key, level3_value in level2_value.items():
                    for level4_key, level4_value in level3_value.items():
                        for level5_key, level5_value in level4_value.items():
                            # Store data in the internal dictionary
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
async def run_server():
    await uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")


# Start the server asynchronously
async def main():
    server_task = asyncio.create_task(run_server())
    
    # Allow some time for the server to start
    await asyncio.sleep(1)

    # Client sends complex JSON to the API
    try:
        url = "http://127.0.0.1:8000/process/"
        nested_json = generate_nested_json()
        async with requests.post(url, json=nested_json) as response:
            print("Response from server:", await response.json())
    except Exception as e:
        print("Error:", e)

    # Stop the server task
    server_task.cancel()

# Run the main function
asyncio.run(main())
