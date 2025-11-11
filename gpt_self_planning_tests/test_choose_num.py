import pytest
from gpt_self_planning_src.choose_num import choose_num

def check(candidate):

    # Check some simple cases
    ret, tot=0, 0
    ret+=(candidate(12, 15) == 14)
    ret+=(candidate(13, 12) == -1)
    ret+=(candidate(33, 12354) == 12354)
    ret+=(candidate(5234, 5233) == -1)
    ret+=(candidate(6, 29) == 28)
    ret+=(candidate(27, 10) == -1)
    tot+=6

    # Check some edge cases that are easy to work out by hand.
    # ret+=candidate(7, 7) == -1
    # ret+=candidate(546, 546) == 546
    return ret/tot



def test_all():
    check(choose_num)
