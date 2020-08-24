# reg_exp.py
"""
Kameron Lightheart
4/30/2019
"""

import re

def reg_exp_playground():
    pattern = re.compile("cat")
    bool(pattern.search("cat"))
    bool(pattern.match("catfish")) # true, starts with cat
    bool(pattern.match("fishcat")) # False, doesn't start with cat
    bool(pattern.search("fishcat")) # True, it does contain cat

    p1, p2 = re.compile(r"^[a-z][^0-7]$"), re.compile(r"^[abcA-C][0-27-9]$")
    for test in ["d8", "aa", "E9", "EE", "d88"]:
        print(test + ":", bool(p1.search(test)), bool(p2.search(test)))

def prob1():
    return re.compile("python")

def prob2():
    return re.compile("\^\{@\}\(\?\)\[%\]\{\.\}\(\*\)\[_\]\{&\}\$")

def test_prob2():
    pattern = prob2()
    print(bool(pattern.match(r"^{@}(?)[%]{.}(*)[_]{&}$")))

def prob3():
    return re.compile("(^Book|^Matress|^Grocery) (store$|supplier$)")

def test_prob3():
    pattern = prob3()
    print(bool(pattern.match("Book store")))
    print(bool(pattern.match("Book supplier")))
    print(bool(pattern.match("Matress store")))
    print(bool(pattern.match("Matress supplier")))
    print(bool(pattern.match("Grocery store")))
    print(bool(pattern.match("Grocery supplier")))
    print(not pattern.match("book store"))
    print(not pattern.match("store"))
    print(not pattern.match("Book"))
    print(not pattern.match("Matress supreme"))

def prob4():
    print("Not implemented")
