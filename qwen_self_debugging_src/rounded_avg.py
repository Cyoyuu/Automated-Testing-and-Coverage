def rounded_avg(n, m):
    if n > m:
        return -1
    average = (n + m) / 2
    rounded = round(average)
    return bin(rounded)
