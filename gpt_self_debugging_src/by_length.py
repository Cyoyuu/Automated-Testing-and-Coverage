def by_length(arr):
    return [["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"][x - 1] for x in sorted([x for x in arr if 1 <= x <= 9])][::-1] if arr else []
