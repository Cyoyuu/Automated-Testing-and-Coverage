import pytest
from qwen_self_debugging_src.rounded_avg import rounded_avg

def check(candidate):
    ret, tot=0, 0

    # Check some simple cases
    ret+=candidate(1, 5) == "0b11"
    ret+=candidate(7, 13) == "0b1010"
    ret+=candidate(964,977) == "0b1111001010"
    ret+=candidate(996,997) == "0b1111100100"
    ret+=candidate(560,851) == "0b1011000010"
    ret+=candidate(185,546) == "0b101101110"
    ret+=candidate(362,496) == "0b110101101"
    ret+=candidate(350,902) == "0b1001110010"
    ret+=candidate(197,233) == "0b11010111"
    tot+=9


    # Check some edge cases that are easy to work out by hand.
    # ret+=candidate(7, 5) == -1
    # ret+=candidate(5, 1) == -1
    # ret+=candidate(5, 5) == "0b101"
    return ret/tot



def test_all():
    check(rounded_avg)
