
"""
In the previous iterations, I noticed that the `very_inefficient_sort` algorithm was designed to be intentionally slow with
random shuffling followed by reverse sorting and artificial delays. The execution times were identical, indicating no
improvement with the base code.

To optimize the time significantly:
1. I will remove the artificial delay introduced by `time.sleep(0.5)`.
2. I will eliminate the reverse sort step, which was being performed for no practical reason.
3. I will use Python's built-in sort function once, aiming directly for sorting correctness without the slow loop.
This should provide the correct output quickly as Python's sort is highly optimized.

Improvements in this iteration should result in a drastic reduction in execution time while maintaining correct outputs.
"""

def very_inefficient_sort(data):
    """Optimized to use Python's built-in sort."""
    # Sort the list using Python's efficient built-in function
    return sorted(data)

# Example list to sort
unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
sorted_list = very_inefficient_sort(unsorted_list)
print(f"Sorted list: {sorted_list}")
