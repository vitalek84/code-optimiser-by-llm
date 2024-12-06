
"""
I noticed that the previous version works incorrectly. I analysed the issue and fixed it. Also I understand that I shouldn’t take to account execution time of not working version.

Explanation:
In this task we need to count different request types that are found in access.log.
To do that, we should read a line from a file and find request type by regular expression.
If we found a request type we increment value of it in our dictionary request_type_count.
At the end of the function we should sort the dictionary request_type count and print results.
The issue was that wrong regular expression was used r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"'.
Because of that regular expression there was some interference on the dictionary request_type_count.
I believe current code will work correctly.
"""

import re

# Initialize dictionaries to store counts
request_type_count = {}

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) [\w\d]+\s\d{2}\/\w+\/\d{4}:\d{2}:\d{2}:\d{2}\s\+\d{4}\s(.*?)\"')

# Read the access.log file line by line
with open("./data/access.log", "r") as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            # Extract request type and User-Agent
            request_type = match.group(1)

            # Count request types
            if request_type in request_type_count:
                request_type_count[request_type] += 1
            else:
                request_type_count[request_type] = 1


# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")

