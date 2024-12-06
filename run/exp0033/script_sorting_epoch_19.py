
def very_inefficient_sort(data):

    def is_sorted(lst):
        """"Check if a list is sorted."""
        for i in range(len(lst) - 1):
            if lst[i] > lst[i + 1]:
                return False
        return True

    unsorted_list = list(data).sort()
    
    if is_sorted(data):
        pass
       
    else:
               
        data = sorted(data)  # Fallback to ensure the result is sorted

    return data


# Example list to sort
unsorted_list = [5, 3, 8, 6, 2, 7, 4, 1]
sorted_list = very_inefficient_sort(unsorted_list)
print(f"Sorted list: {sorted_list}")
