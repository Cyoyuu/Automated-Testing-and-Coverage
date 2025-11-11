def choose_num(x, y):
    for num in range(min(x, y), max(x, y) + 1)[::-1]:
        if num % 2 == 0:
            return num
    return -1
