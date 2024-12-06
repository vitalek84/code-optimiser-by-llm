
"""
I noticed that the previous version works incorrectly. I analysed the issue and fixed it. Also I understand that I shouldn’t take to account execution time of not working version

This script calculates request type counts in the access.log file.
It uses a regular expression to extract the request type and User-Agent from each line in the file.
The request type is then counted and stored in a dictionary.
The dictionary is sorted in descending order and the results are printed.
I expect that it will work faster because sorting the dictionary of structured items uses less space
"""


import re

# Initialize dictionaries to store counts
request_type_count = {}

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\"')

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

