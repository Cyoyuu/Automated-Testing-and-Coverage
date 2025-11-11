def move_one_ball(arr):
    if not arr:
        return True
    drops = 0
    n = len(arr)
    for i in range(n):
        if arr[i] > arr[(i + 1) % n]:
            drops += 1
    return drops <= 1
