
"""
Chain of thought:
1. The previous code reads the file line by line, which is already efficient for processing large files.
2. However, we can optimize the regular expression matching and dictionary operations to potentially reduce execution time.
3. Using a defaultdict from the collections module can simplify the counting logic.
4. We can also pre-compile the regular expression outside of the loop if it doesn't change, which is already done in the original code.
5. Let's try using a more efficient way to count the request types and see if it improves performance.
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

            # Count request types using defaultdict
            request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
