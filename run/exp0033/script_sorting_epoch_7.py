
import random
import time

def very_inefficient_sort(data):
    def is_sorted(lst):
        """Check if a list is sorted."""
        for i in range(len(lst) - 1):
            if lst[i] > lst[i + 1]:
                return False
        return True
    
    def reverse_sort(lst):
        """Sort the list in reverse order using bubble sort for inefficiency."""
        n = len(lst)
        for i in range(n):
            for j in range(n - i - 1):
                if lst[j] < lst[j + 1]:
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
        return lst

    max_iterations = 40  # Maximum number of iterations to avoid infinite loops
    iteration = 0
    intensity = 1.0  # Start with full shuffle intensity

    while not is_sorted(data) and iteration < max_iterations:
        # Waste time by reverse-sorting the list (which we will shuffle anyway)
        # print(f"Iteration {iteration + 1}: Reverse sorting: {data}")
        data = reverse_sort(data)

        # Randomly shuffle the list with decreasing intensity
        # print(f"Iteration {iteration + 1}: Shuffling with intensity {intensity:.2f}")
        data = random.shuffle(data)

        # Add an artificial delay for fun
        time.sleep(0.5)

        # Reduce shuffle intensity over time to increase sorting likelihood
        intensity = max(0.1, intensity * 0.9)

        iteration += 1

    if is_sorted(data):
        pass
        # print("Successfully sorted!")
    else:
        # print("Max iterations reached. Final attempt to sort...")
        data = sorted(data)  # Fallback to ensure the result is sorted

    return data

# Example list to sort
unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
sorted_list = very_inefficient_sort(unsorted_list)
print(f"Sorted list: {sorted_list}")
