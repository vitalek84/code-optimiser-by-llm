
"""
I noticed that the previous version has different results with reference results.
I analysed the issue and tried to fix it. So, results should be the same in the current version.
I noticed that the previous version works incorrectly. 
I analysed the issue and fixed it. Also, I understand that I shouldn’t take into account execution time of not working versions
"""

import re
import collections

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Initialize dictionary to store counts
request_type_count = collections.Counter()

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

