def by_length(arr):
    digits = {"One":1,"Two":2,"Three":3,"Four":4,"Five":5,"Six":6,"Seven":7,"Eight":8,"Nine":9}
    sorted_arr = sorted([x for x in arr if 1 <= x <= 9], reverse=True)
    return [k for v in sorted_arr for k, val in digits.items() if val == v]
