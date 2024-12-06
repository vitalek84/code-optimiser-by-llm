
# Import the necessary libraries
import collections
import re

# Initialize a Counter object to store the request type counts
request_type_count = collections.Counter()

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
            request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = request_type_count.most_common()

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count:
    print(f"{request_type}: {count}")
