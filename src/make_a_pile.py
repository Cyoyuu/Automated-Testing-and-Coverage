def make_a_pile(n):
    result = []
    current = n
    for _ in range(n):
        result.append(current)
        current += 2
    return result
