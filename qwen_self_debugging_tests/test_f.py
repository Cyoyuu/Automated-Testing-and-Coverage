import pytest
from qwen_self_debugging_src.f import f

def check(candidate):
    ret, tot=0, 0

    ret+=(candidate(5) == [1, 2, 6, 24, 15])
    ret+=(candidate(7) == [1, 2, 6, 24, 15, 720, 28])
    ret+=(candidate(1) == [1])
    ret+=(candidate(3) == [1, 2, 6])
    tot+=4
    return ret/tot


def test_all():
    check(f)
