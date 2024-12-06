
"""
Optimizing the script by using more efficient data structures and reducing the overhead of function calls.
In this version, I use `collections.Counter` to count occurrences, which is faster than manually updating a dictionary.
Additionally, I eliminate the lambda function for sorting as `Counter.most_common` provides the desired result directly.
"""

import re
from collections import Counter

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Initialize a counter to store counts
request_type_count = Counter()

# Read the access.log file line by line
with open("./data/access.log", "r") as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            # Extract request type and User-Agent
            request_type = match.group(1)
            request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = request_type_count.most_common()

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count:
    print(f"{request_type}: {count}")
