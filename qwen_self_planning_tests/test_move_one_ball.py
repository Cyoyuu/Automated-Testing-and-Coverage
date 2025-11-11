import pytest
from qwen_self_planning_src.move_one_ball import move_one_ball

def check(candidate):
    ret, tot=0, 0

    # Check some simple cases
    ret+=candidate([3, 4, 5, 1, 2])==True
    ret+=candidate([3, 5, 10, 1, 2])==True
    ret+=candidate([4, 3, 1, 2])==False
    ret+=candidate([1, 2, 3, 4, 5]) == True
    ret+=candidate([5, 1, 2, 3, 4]) == True
    ret+=candidate([2, 3, 4, 5, 1]) == True
    ret+=candidate([3, 4, 5, 1, 2]) == True
    ret+=candidate([4, 5, 1, 2, 3]) == True
    ret+=candidate([5, 4, 3, 2, 1]) == False
    ret+=candidate([1, 3, 2, 4, 5]) == False
    ret+=candidate([]) == True
    ret+=candidate([1]) == True
    ret+=candidate([2, 1]) == True
    ret+=candidate([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]) == False
    ret+=candidate([1, 10, 9, 8, 7, 6, 5, 4, 3, 2]) == True
    tot+=15
    return ret/tot


def test_all():
    return check(move_one_ball)
