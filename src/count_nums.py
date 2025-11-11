def count_nums(arr):
    def digit_sum(num):
        s = sum(int(d) for d in str(abs(num)))
        return s if num >= 0 else s - 2 * int(str(abs(num))[0])
    return sum(1 for x in arr if digit_sum(x) > 0)
