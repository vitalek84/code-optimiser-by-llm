
"""
The script currently utilizes a highly inefficient sorting algorithm that randomly shuffles the list and performs unnecessary operations like reverse sorting with bubble sort and adding sleep delay. 
The task is to drastically reduce the execution time while still achieving the sorted result as the reference results.
I will implement the built-in Python sort function, which is highly optimized, and remove unnecessary code to optimize execution time.
"""

def very_inefficient_sort(data):
    return sorted(data)

# Example list to sort
unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
sorted_list = very_inefficient_sort(unsorted_list)
print(f"Sorted list: {sorted_list}")
