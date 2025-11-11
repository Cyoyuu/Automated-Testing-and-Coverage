import pytest
from gpt_self_planning_src.by_length import by_length

def check(candidate):

    # Check some simple cases
    ret, tot=0, 0
    ret+= (candidate([2, 1, 1, 4, 5, 8, 2, 3]) == ["Eight", "Five", "Four", "Three", "Two", "Two", "One", "One"])
    ret+= (candidate([]) == [])
    ret+= (candidate([1, -1 , 55]) == ['One'])
    tot+=3

    # Check some edge cases that are easy to work out by hand.
    # assert True, "This prints if this assert fails 2 (also good for debugging!)"
    # ret+=candidate([1, -1, 3, 2]) == ["Three", "Two", "One"]
    # ret+=candidate([9, 4, 8]) == ["Nine", "Eight", "Four"]
    return ret/tot



def test_all():
    return check(by_length)
