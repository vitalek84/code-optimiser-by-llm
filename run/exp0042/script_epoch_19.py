
"""
I noticed that the previous version worked as expected but there was no optimization in terms of performance.
In this version, I will try to use the `collections.Counter` for counting request types and avoid checking condition in 
each iteration, to potentially speed up counting with direct updates. I will also use list comprehension to perform
all matches first and then count them, this should reduce the number of executions of the regex. 
"""

import re
from collections import Counter

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Initialize Counter to store counts
request_type_count = Counter()

# Read the access.log file content at once and use list comprehension to find all matches
with open("./data/access.log", "r") as file:
    matches = (log_pattern.search(line) for line in file)
    request_types = (match.group(1) for match in matches if match)
    request_type_count.update(request_types)

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
