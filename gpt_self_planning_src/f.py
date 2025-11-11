def f(n):
    results = []
    for i in range(1, n + 1):
        if i % 2 == 0:
            factorial = 1
            for j in range(1, i + 1):
                factorial *= j
            results.append(factorial)
        else:
            results.append(sum(range(1, i + 1)))
    return results
