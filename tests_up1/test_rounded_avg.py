import pytest
from src.rounded_avg import rounded_avg

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
    ret+=candidate(0, 0) == "0b0"
    ret+=candidate(-1, -1) == "0b-1"
    ret+=candidate(2, 2) == "0b10"
    ret+=candidate(1, 3) == "0b10"
    ret+=candidate(1, 4) == "0b11"
    ret+=candidate(1, 5) == "0b11"
    ret+=candidate(1, 6) == "0b110"
    ret+=candidate(1, 7) == "0b111"
    ret+=candidate(1, 8) == "0b1000"
    ret+=candidate(1, 9) == "0b1001"
    ret+=candidate(1, 10) == "0b1010"
    ret+=candidate(1, 11) == "0b1011"
    ret+=candidate(1, 12) == "0b1100"
    ret+=candidate(1, 13) == "0b1101"
    ret+=candidate(1, 14) == "0b1110"
    ret+=candidate(1, 15) == "0b1111"
    ret+=candidate(1, 16) == "0b10000"
    ret+=candidate(1, 17) == "0b10001"
    ret+=candidate(1, 18) == "0b10010"
    ret+=candidate(1, 19) == "0b10011"
    ret+=candidate(1, 20) == "0b10100"
    ret+=candidate(1, 21) == "0b10101"
    ret+=candidate(1, 22) == "0b10110"
    ret+=candidate(1, 23) == "0b10111"
    ret+=candidate(1, 24) == "0b11000"
    ret+=candidate(1, 25) == "0b11001"
    ret+=candidate(1, 26) == "0b11010"
    tot+=36
    return ret/tot


def test_all():
    return check(rounded_avg)
