
"""
I noticed that the current version's execution time is unchanged from the base version. 
To optimize it, I will:
1. Use the `collections` module to make counting operations more efficient using `defaultdict`.
2. Use iterator approaches to potentially streamline the file reading and processing.
3. Pre-compile the regular expression, which was already done, but ensure it's used optimally.
"""

import re
from collections import defaultdict

# Initialize defaultdict to store counts
request_type_count = defaultdict(int)

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Efficiently read the file in a single pass
with open("./data/access.log", "r") as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            # Extract request type
            request_type = match.group(1)
            # Count request types
            request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
