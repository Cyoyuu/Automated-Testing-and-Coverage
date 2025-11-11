def make_a_pile(n):
    pile = []
    current = n
    for _ in range(n):
        pile.append(current)
        if n % 2 == 0:
            current += 2
        else:
            current += 2
    return pile
