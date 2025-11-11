def rounded_avg(n, m):
    if n > m:
        return -1
    total = sum(range(n, m + 1))
    average = total / (m - n + 1)
    rounded = round(average)
    return bin(rounded)
