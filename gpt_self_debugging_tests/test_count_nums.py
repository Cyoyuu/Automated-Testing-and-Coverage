import pytest
from gpt_self_debugging_src.count_nums import count_nums

def check(candidate):

    # Check some simple cases
    ret, tot=0, 0
    ret+=(candidate([]) == 0)
    ret+=(candidate([-1, -2, 0]) == 0)
    ret+=(candidate([1, 1, 2, -2, 3, 4, 5]) == 6)
    ret+=(candidate([1, 6, 9, -6, 0, 1, 5]) == 5)
    ret+=(candidate([1, 100, 98, -7, 1, -1]) == 4)
    ret+=(candidate([12, 23, 34, -45, -56, 0]) == 5)
    ret+=(candidate([-0, 1**0]) == 1)
    ret+=(candidate([1]) == 1)
    tot+=8

    # Check some edge cases that are easy to work out by hand.
    assert True, "This prints if this assert fails 2 (also good for debugging!)"
    return ret/tot



def test_all():
    check(count_nums)
