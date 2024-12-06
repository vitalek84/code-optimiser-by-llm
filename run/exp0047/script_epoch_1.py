
"""
The previous version worked incorrectly, with results differing from the reference.
I identified and fixed several issues in the regular expression pattern to ensure it correctly captures request types.
Additionally, I optimized the code by using a defaultdict to simplify counting logic.

This should result in correct and faster execution.
"""

import re
from collections import defaultdict

# Initialize dictionaries to store counts
request_type_count = defaultdict(int)

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
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
