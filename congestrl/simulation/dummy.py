import random


def split_numbers_into_sublists(numbers, n):
    # Shuffle the list to ensure random distribution
    shuffled = numbers.copy()
    random.shuffle(shuffled)

    # Calculate the base size and the number of sublists needing an extra element
    total_numbers = len(shuffled)
    base_size = total_numbers // n
    remainder = total_numbers % n

    sublists = {}
    start = 0

    for i in range(1, n + 1):
        # Determine the size of the current sublist
        if i <= remainder:
            sublist_size = base_size + 1
        else:
            sublist_size = base_size

        # Slice the shuffled list to get the sublist
        end = start + sublist_size
        sublist = shuffled[start:end]

        # Sort the sublist for better readability (optional)
        sublist.sort()

        sublists[i] = sublist
        start = end

    return sublists


# Example usage
numbers = list(range(1, 11))  # [1, 2, 3, ..., 10]
n = 3
result = split_numbers_into_sublists(numbers, n)
print(result)