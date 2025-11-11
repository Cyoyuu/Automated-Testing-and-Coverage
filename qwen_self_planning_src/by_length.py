def by_length(arr):
    return list(map(lambda x: ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"][x-1], reversed(sorted([num for num in arr if 1 <= num <= 9]))))
