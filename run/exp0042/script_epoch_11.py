
"""
To optimize the code for improved execution time, I have taken the following steps:
1. Used the 'collections' module's 'defaultdict' to handle counting, which eliminates the need for an if-else construct checking the existence of request types.
2. This refactoring results in cleaner and potentially faster code since 'defaultdict' automatically initializes missing keys with a default value.
3. Moved the regular expression compilation outside of the loop to avoid repeated compilation.
4. Gathered lines in a list from the file and then processed, which can sometimes leverage better IO handling instead of line-by-line processing.
5. Ensured that the basic logic and result structure remain the same.
"""

import re
from collections import defaultdict

# Initialize defaultdict to store counts
request_type_count = defaultdict(int)

# Regular expression to extract request type
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the access.log file all at once
with open("./data/access.log", "r") as file:
    lines = file.readlines()
    
for line in lines:
    match = log_pattern.search(line)
    if match:
        # Extract request type
        request_type = match.group(1)

        # Count request types using defaultdict
        request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
