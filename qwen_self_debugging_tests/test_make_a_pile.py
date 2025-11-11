import pytest
from qwen_self_debugging_src.make_a_pile import make_a_pile

def check(candidate):
    ret, tot=0, 0

    # Check some simple cases
    ret+=(candidate(3) == [3, 5, 7])
    ret+=(candidate(4) == [4,6,8,10])
    ret+=(candidate(5) == [5, 7, 9, 11, 13])
    ret+=(candidate(6) == [6, 8, 10, 12, 14, 16])
    ret+=(candidate(8) == [8, 10, 12, 14, 16, 18, 20, 22])
    tot+=5

    # Check some edge cases that are easy to work out by hand.
    assert True, "This prints if this assert fails 2 (also good for debugging!)"
    return ret/tot



def test_all():
    check(make_a_pile)
