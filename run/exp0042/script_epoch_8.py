
"""
I looked at the provided script which uses regular expressions to parse each line of a file. This can be quite slow for large files.
I have observed that the performance gain could be obtained by using more efficient parsing, if possible.
In this case, we can use the 'collections.Counter' to simplify counting and potentially optimize operations by reducing the dictionary operations for counting.
Also, I am utilizing 'with open' as it is and the compiled regular expression since there is not much improvement possible without changing the fundamental approach.
"""

import re
from collections import Counter

# Initialize Counter to store counts
request_type_count = Counter()

# Regular expression to extract request type
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the access.log file line by line
with open("./data/access.log", "r") as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            # Extract request type
            request_type = match.group(1)
            request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
