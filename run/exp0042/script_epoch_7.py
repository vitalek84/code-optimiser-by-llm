
"""
I will attempt to improve the performance of the script by using the 'collections' module, specifically the 'defaultdict' and 'Counter' classes. 
'Counter' can simplify counting and 'defaultdict' can simplify the dictionary operations. Furthermore, to avoid opening and reading large files, 
I'll implement reading chunks from the file if possible which can reduce the memory footprint and speed up the processing. 
Using these Python standard libraries usually leads to more efficient code. I'll also remove the explicit declaration and initialization of 
the dictionary for counting request types.
"""

import re
from collections import Counter

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

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
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
