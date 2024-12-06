import re
import collections
import io

# Initialize a namedtuple for storing counts
RequestTypeCount = collections.namedtuple("RequestTypeCount", ["type", "count"])

# Write results in more effective way - in-memory file like object
results_file = io.StringIO()

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the access.log file line by line
with open("./data/access.log", "r") as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            # Extract request type and User-Agent
            request_type = match.group(1)

            # Count request types
            count = request_type_count[request_type] if request_type in request_type_count else 0
            request_type_count[request_type] = count + 1


# Sort the counts in descending order
sorted_request_type_count = sorted(request_type_count.items(), key=lambda item: item[1], reverse=True)

# Print the results into in-memory file like object
results_file.write("Request Type Counts:\n")
for request_type, count in sorted_request_type_count:
    results_file.write(f"{request_type}: {count}\n")

print(results_file.getvalue())

