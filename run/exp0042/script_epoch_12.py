
"""
Optimization Strategy:
1. Utilize the `collections.Counter` class for more efficient counting of request types from the log file.
2. Remove individual if-else checks for counting occurrences and delegate this task to `Counter`.
3. Reduce the number of lookups by using list comprehensions and direct Counter functionality.
"""

import re
from collections import Counter

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Initialize Counter to store counts directly
request_type_count = Counter()

# Read the access.log file line by line
with open("./data/access.log", "r") as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            # Extract request type
            request_type = match.group(1)
            # Update count using Counter
            request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = dict(request_type_count.most_common())

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
