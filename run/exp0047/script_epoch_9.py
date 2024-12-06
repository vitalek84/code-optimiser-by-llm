
"""
Chain of thought:
- The initial script reads the file line by line and uses regular expressions to extract request types.
- To improve performance, we can read the entire file into memory at once, which reduces the overhead of opening and reading the file multiple times.
- We'll also use a defaultdict to simplify counting request types.
- Additionally, we'll use the Counter class from collections, which is optimized for counting hashable objects.
"""

from collections import Counter
import re
from collections import defaultdict

# Initialize a Counter to store counts
request_type_count = Counter()

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the entire access.log file into memory at once
with open("./data/access.log", "r") as file:
    content = file.read()
    lines = content.splitlines()

# Process all lines at once
for line in lines:
    match = log_pattern.search(line)
    if match:
        # Extract request type and User-Agent
        request_type = match.group(1)

        # Count request types
        request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
