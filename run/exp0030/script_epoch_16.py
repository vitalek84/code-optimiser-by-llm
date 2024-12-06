
"""
The previous version works incorrectly. There was an error while the program tried to sort the dictionary request_type_count where keys are string but operation tried to apply for int keys. 
In current approach used lambda that takes key and value together.
"""
import re

# Initialize dictionaries to store counts
request_type_count = {}

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the access.log file line by line
with open("./data/access.log", "r") as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            # Extract request type and User-Agent
            request_type = match.group(1)

            # Count request types
            if request_type in request_type_count:
                request_type_count[request_type] += 1
            else:
                request_type_count[request_type] = 1

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: (item[1], item[0]), reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
