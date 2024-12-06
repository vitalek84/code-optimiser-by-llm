
"""
The dataset contains a huge access.log file. The file contains log records where each line describes an incoming HTTP request to a web server and consists of many fields, among which are request type and User-Agent header. In the base version the full logs are stored in a memory to calculate request 
type counts, this cannot be optimised in terms of memory hence we need to do it line by line.
The first optimisation that came to mind was to move to a generator instead of reading the whole file into memory, this will save a lot of time. Right now a re.search happens on each and every line, but we can certainly capture everything in the group when iterating through the file line by line. Moving the sorting operation before we capture everything into the dictionary will save us from sorting the dictionary in descending order in the end.
"""
import re

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Initialize request type count
request_type_count = {}

# Generator function to read the access.log file line by line
def read_log_file(filename):
    with open(filename, "r") as file:
        for line in file:
            yield line

# Iterate over the generator
for line in read_log_file("./data/access.log"):
    match = log_pattern.search(line)
    if match:
        # Extract request type
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

