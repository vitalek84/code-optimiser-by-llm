"""
This is my first optimization attempt. Here's my chain of thought:

1. The main performance bottleneck is the intentional time.sleep(0.5) which adds 500ms delay per iteration
2. The reverse_sort function using bubble sort is inefficient O(n^2)
3. The shuffle function is unnecessary since we're trying to sort
4. The is_sorted check is O(n) but not a major concern for small lists
5. The whole approach of randomly shuffling and reverse sorting is inefficient
6. We can replace everything with Python's built-in sorted() function
7. No need for any iterations or checks since sorted() guarantees the result

The optimization removes all intentional inefficiencies while maintaining the same output.
"""

def very_inefficient_sort(data):
    return sorted(data)

# Example list to sort
unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
sorted_list = very_inefficient_sort(unsorted_list)
print(f"Sorted list: {sorted_list}")