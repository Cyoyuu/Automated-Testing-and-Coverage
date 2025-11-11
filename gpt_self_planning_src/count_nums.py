def count_nums(arr):
    counter = 0
    for num in arr:
        digit_sum = sum(int(d) if num >= 0 else -int(d) for d in str(abs(num)))
        if digit_sum > 0:
            counter += 1
    return counter
