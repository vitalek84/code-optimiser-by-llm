
"""
I noticed that the results of the reference version and my previous version are different, I analysed the issue and tried to fix it.
In this iteration, I will try to optimize the code execution time by using collections.Counter which is optimized for counting hashable objects like strings.
This should reduce the time required for counting request types compared to a dictionary.
For regular expression optimization, pre-compiled patterns are already being used which is optimal.
Additionally, using the sorted function directly on list of tuples rather than converting it back to a dictionary might improve performance.
"""

import re
from collections import Counter

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Initialize Counter to store request types
request_type_count = Counter()

# Read the access.log file line by line
with open("./data/access.log", "r") as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            # Extract request type
            request_type = match.group(1)
            # Increment count for request type
            request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = sorted(request_type_count.items(), key=lambda item: item[1], reverse=True)

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count:
    print(f"{request_type}: {count}")
