def unique_digits(x):
    res = []
    for num in x:
        digits = str(num)
        if all(int(d) % 2 != 0 for d in digits):
            res.append(num)
    return sorted(res)
