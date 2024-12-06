
import collections.abc

# Define a custom class to capture line-related state
class RegexMatch:
    def __init__(self, match):
        self.match = match
        self.request_type = match.group(1)
        self.user_agent = match.group(2)


# Initialize dictionaries to store counts, mapping request types and user agents to counts
request_type_count = collections.Counter()
user_agent_count = collections.Counter()

# Initialize a dictionary to store RegexMatch objects, mapping line numbers to matches
line_matches = {}

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

# Read the access.log file line by line
with open("./data/access.log", "r") as file:
    line_number = 0
    for line in file:
        match = log_pattern.search(line)
        if match:
            line_matches[line_number] = RegexMatch(match)
        line_number += 1

# Count request types and user agents for each line number
for line_number, match in line_matches.items():
    request_type_count[match.request_type] += 1
    user_agent_count[match.user_agent] += 1

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))
sorted_user_agent_count = dict(sorted(user_agent_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")

print("\nUser Agent Counts:")
for user_agent, count in sorted_user_agent_count.items():
    print(f"{user_agent}: {count}")
