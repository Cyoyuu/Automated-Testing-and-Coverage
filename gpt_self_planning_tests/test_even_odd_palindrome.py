import pytest
from gpt_self_planning_src.even_odd_palindrome import even_odd_palindrome

def check(candidate):

    # Check some simple cases
    ret, tot=0, 0
    ret+=(candidate(123) == (8, 13))
    ret+=(candidate(12) == (4, 6))
    ret+=(candidate(3) == (1, 2))
    ret+=(candidate(63) == (6, 8))
    ret+=(candidate(25) == (5, 6))
    ret+=(candidate(19) == (4, 6))
    ret+=(candidate(9) == (4, 5))
    tot+=7

    # Check some edge cases that are easy to work out by hand.
    # ret+=candidate(1) == (0, 1), "This prints if this assert fails 2 (also good for debugging!)"
    return ret/tot



def test_all():
    check(even_odd_palindrome)
