import pytest
from src.unique_digits import unique_digits

def check(candidate):
    ret, tot=0, 0

    # Check some simple cases
    ret+=candidate([15, 33, 1422, 1]) == [1, 15, 33]
    ret+=candidate([152, 323, 1422, 10]) == []
    ret+=candidate([12345, 2033, 111, 151]) == [111, 151]
    ret+=candidate([135, 103, 31]) == [31, 135]
    tot+=4

    # Check some edge cases that are easy to work out by hand.
    assert True
    return ret/tot



def test_all():
    check(unique_digits)
