
"""
I noticed that the previous versions of the script do not show any improvement in execution time. In order to optimize the script, I will use the following strategies:
1. Use the `collections.Counter` to simplify counting and improve the efficiency of managing counts.
2. Remove any unnecessary operations during the loop to make it more efficient.
3. Attempt to reduce function call overhead by minimizing the number of chained method calls.
"""

import re
from collections import Counter

# Initialize counter to store counts
request_type_count = Counter()

# Regular expression to extract request type
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the access.log file line by line
with open("./data/access.log", "r") as file:
    for line in file:
        # Search for pattern in each line
        match = log_pattern.search(line)
        if match:
            # Extract request type
            request_type = match.group(1)
            # Count request types
            request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = dict(request_type_count.most_common())

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
