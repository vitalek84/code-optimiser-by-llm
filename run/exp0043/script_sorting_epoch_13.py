
"""
To optimize the performance, I've removed unnecessary inefficiencies and delays in the sorting algorithm. Here's how I approached it:
1. Removed the artificial sleep delay to speed up the sorting process.
2. Replaced the inefficient reverse sorting and shuffle mechanism with Python's built-in sorting.
3. Kept the check for a sorted list to maintain logic, but will only use Python's built-in sort as a fallback.
4. The goal is to achieve significant reductions in execution time by leveraging efficient built-in functionality.
"""

import random


def very_inefficient_sort(data):
    def is_sorted(lst):
        """Check if a list is sorted."""
        for i in range(len(lst) - 1):
            if lst[i] > lst[i + 1]:
                return False
        return True

    # The modifications start here
    if not is_sorted(data):
        # Directly use built-in sorting as a more efficient approach
        data = sorted(data)
    
    return data


# Example list to sort
unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
sorted_list = very_inefficient_sort(unsorted_list)
print(f"Sorted list: {sorted_list}")
