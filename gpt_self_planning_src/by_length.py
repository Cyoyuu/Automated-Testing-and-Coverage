def by_length(arr):
    names = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    return [names[i] for i in sorted([x for x in arr if 1 <= x <= 9], reverse=True)]
