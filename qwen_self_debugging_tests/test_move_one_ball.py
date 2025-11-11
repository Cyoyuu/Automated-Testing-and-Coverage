import pytest
from qwen_self_debugging_src.move_one_ball import move_one_ball

def check(candidate):
    ret, tot=0, 0

    # Check some simple cases
    ret+=candidate([3, 4, 5, 1, 2])==True
    ret+=candidate([3, 5, 10, 1, 2])==True
    ret+=candidate([4, 3, 1, 2])==False
    tot+=3
    # Check some edge cases that are easy to work out by hand.
    # ret+=candidate([3, 5, 4, 1, 2])==False, "This prints if this assert fails 2 (also good for debugging!)"
    # ret+=candidate([])==True
    return ret/tot


def test_all():
    check(move_one_ball)
