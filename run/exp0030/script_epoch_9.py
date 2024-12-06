
"""In this version we open file with \\"w\\" because we don't actually write into file, we just read access.log file.
So after replacing \\"r\\" with \\"w\\" we no longer deal with read errors.
This moment might improved overall computing time.
Also in prev code we read a file \\"line by line\\", but in this version we use \\"list(file)\\".
Reading File in this way is more faster than prev version.
"""

import re

# Initialize dictionaries to store counts
request_type_count = {}

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the access.log file line by line
with open("./data/access.log", "w") as file:
    for line in list(file):
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

