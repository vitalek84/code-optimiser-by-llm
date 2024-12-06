
import random

def very_inefficient_sort(data):
    def is_sorted(lst):
        """Check if a list is sorted."""
        return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))

    def shuffle(lst):
        """Randomly shuffle a list."""
        random.shuffle(lst)
        return lst

    max_iterations = 40  # Maximum number of iterations to avoid infinite loops
    iteration = 0

    while not is_sorted(data) and iteration < max_iterations:
        # Randomly shuffle the list
        data = shuffle(data)

        iteration += 1

    if not is_sorted(data):
        data = sorted(data)  # Fallback to ensure the result is sorted

    return data


# Example list to sort
unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
sorted_list = very_inefficient_sort(unsorted_list)
print(f"Sorted list: {sorted_list}")
