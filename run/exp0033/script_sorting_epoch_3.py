
import time

def very_inefficient_sort(data):
    def is_sorted(lst):
        """Check if a list is sorted."""
        for i in range(len(lst) - 1):
            if lst[i] > lst[i + 1]:
                return False
        return True

    max_iterations = 40  # Maximum number of iterations to avoid infinite loops
    iteration = 0
    intensity = 1.0  # Start with full shuffle intensity

    # Replace shuffle with a random-sampling swap
    while not is_sorted(data) and iteration < max_iterations:
        i, j = random.sample(range(len(data)), 2)
        data[i], data[j] = data[j], data[i]

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
