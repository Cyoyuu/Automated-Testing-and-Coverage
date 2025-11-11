def make_a_pile(n):
    return [n + 2 * i for i in range(n)] if n % 2 == 1 else [n + 2 * i for i in range(n)]
