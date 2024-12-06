
"""
I noticed that the previous version had the same execution time as the base code, and the results were identical. To improve performance, I will try to use a single-threaded server instead of spawning a new thread for the server. This is because thread spawning and synchronization could add overhead. I will set 'workers=1' when starting uvicorn to force a single worker. Another minor speedup can be achieved by reducing the function's scope that assigns to the global 'internal_dict' variable, as repeated dictionary initialization could be a performance bottleneck.
"""

from fastapi import FastAPI
import uvicorn
import requests
import time

# Define the FastAPI app
app = FastAPI()

# Internal storage dictionary
internal_dict = {}

# Endpoint for processing complex JSON
@app.post("/process/")
async def process_item(data: dict):
    nonlocal_dict = {}  # Local dictionary for data processing
    element_count = 0

    try:
        # Nested loops to process the JSON
        for level1_key, level1_value in data.items():
            for level2_key, level2_value in level1_value.items():
                for level3_key, level3_value in level2_value.items():
                    for level4_key, level4_value in level3_value.items():
                        for level5_key, level5_value in level4_value.items():
                            # Store data in the nonlocal dictionary and update global one
                            key = f"{level1_key}.{level2_key}.{level3_key}.{level4_key}.{level5_key}"
                            nonlocal_dict[key] = level5_value
                            element_count += 1
                            
        # Update global internal_dict once
        global internal_dict
        internal_dict = nonlocal_dict
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
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning", workers=1)


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
