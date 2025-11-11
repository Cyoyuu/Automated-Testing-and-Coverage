def by_length(arr):
    names = ['One','Two','Three','Four','Five','Six','Seven','Eight','Nine']
    filtered = [n for n in arr if 1 <= n <= 9]
    filtered.sort()
    filtered.reverse()
    return [names[n-1] for n in filtered]
