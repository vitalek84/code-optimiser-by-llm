
"""
In this version, I am attempting to optimize the execution time of the script by using the built-in 'collections' module's 'Counter' class, which is more efficient for counting occurrences in a collection. This should help in reducing the execution time compared to manual dictionary updates. Additionally, to further improve the code, I will switch to using compiled regular expressions with alternative patterns if possible. I will also ensure to buffer the file reading to optimize I/O operations.
"""

import re
from collections import Counter

# Regular expression to extract request type
log_pattern = re.compile(r'\"(\w+) /')

# Initialize Counter to store counts
request_type_count = Counter()

# Read the access.log file line by line
with open("./data/access.log", "r") as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            # Extract request type
            request_type = match.group(1)
            # Count request types using Counter
            request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = dict(request_type_count.most_common())

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
