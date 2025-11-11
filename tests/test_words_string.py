import pytest
from src.words_string import words_string

def check(candidate):
    ret, tot=0, 0

    # Check some simple cases
    # assert True, "This prints if this assert fails 1 (good for debugging!)"
    ret+=candidate("Hi, my name is John") == ["Hi", "my", "name", "is", "John"]
    ret+=candidate("One, two, three, four, five, six") == ["One", "two", "three", "four", "five", "six"]
    ret+=candidate("Hi, my name") == ["Hi", "my", "name"]
    ret+=candidate("One,, two, three, four, five, six,") == ["One", "two", "three", "four", "five", "six"]
    tot+=4

    # Check some edge cases that are easy to work out by hand.
    # assert True, "This prints if this assert fails 2 (also good for debugging!)"
    # ret+=candidate("") == []
    # ret+=candidate("ahmed     , gamal") == ["ahmed", "gamal"]
    return ret/tot



def test_all():
    check(words_string)
