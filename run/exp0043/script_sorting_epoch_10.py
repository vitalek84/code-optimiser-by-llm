
"""
I noticed that the execution time of the initial script is high due to the artificial time delay (sleep) and the inefficient sorting techniques employed such as reverse bubble sort and random shuffling to simulate inefficiency. To optimize the execution time in this new version, I've removed the artificial delay and highly inefficient reverse bubble sort and shuffle logic. Instead, I've implemented a straightforward sorting technique to achieve the desired result rapidly, without altering the correctness of the output.
"""

def very_efficient_sort(data):
    return sorted(data)

# Example list to sort
unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
sorted_list = very_efficient_sort(unsorted_list)
print(f"Sorted list: {sorted_list}")
