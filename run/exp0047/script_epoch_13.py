
"""
First optimization attempt:
- Use a more efficient way to count occurrences by using collections.Counter.
- Compile the regex pattern only once outside the loop.
"""

import re
from collections import Counter

# Initialize dictionary to store counts
request_type_count = Counter()

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the access.log file line by line
with open("./data/access.log", "r") as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            # Extract request type and User-Agent
            request_type = match.group(1)

            # Count request types using Counter
            request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = dict(request_type_count.most_common())

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
