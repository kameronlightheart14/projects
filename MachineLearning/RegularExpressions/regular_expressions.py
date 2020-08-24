# regular_expressions.py
"""Volume 3: Regular Expressions.
Kameron Lightheart
MATH 403
4/30/2019
"""

import re

# Problem 1
def prob1():
    """Compile and return a regular expression pattern object with the
    pattern string "python".

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    return re.compile("python")

# Problem 2
def prob2():
    """Compile and return a regular expression pattern object that matches
    the string "^{@}(?)[%]{.}(*)[_]{&}$".

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    return re.compile(r"\^\{@\}\(\?\)\[%\]\{\.\}\(\*\)\[_\]\{&\}\$")

# Problem 3
def prob3():
    """Compile and return a regular expression pattern object that matches
    the following strings (and no other strings).

        Book store          Mattress store          Grocery store
        Book supplier       Mattress supplier       Grocery supplier

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    return re.compile("^(Book|Mattress|Grocery) (store|supplier)$")

# Problem 4
def prob4():
    """Compile and return a regular expression pattern object that matches
    any valid Python identifier.

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    py_id = r"([a-z]|[A-Z]|_)\w*" # Python identifier
    real_num = r"-?\d*(.\d*)?"
    string = r"(\'(^\')*\')"

    # Start with valid python var
    return re.compile(r"^" + py_id           
        # Followed by any number of spaces
        + r" *"                              
        # Optional followed by equals real number or string
        + r"(= *(" + real_num + "|" + string + "|" + py_id + r"))?$")

# Problem 5
def prob5(code):
    """Use regular expressions to place colons in the appropriate spots of the
    input string, representing Python code. You may assume that every possible
    colon is missing in the input string.

    Parameters:
        code (str): a string of Python code without any colons.

    Returns:
        (str): code, but with the colons inserted in the right places.
    """
    # Define a regex to find all the lines of code that need a colon
    search_str = r"(\s*(while|if|elif|else|for|while|try|except|finally|with|def|class).*)"
    return re.sub(search_str, r"\1:", code)

# Problem 6
def prob6(filename="fake_contacts.txt"):
    """Use regular expressions to parse the data in the given file and format
    it uniformly, writing birthdays as mm/dd/yyyy and phone numbers as
    (xxx)xxx-xxxx. Construct a dictionary where the key is the name of an
    individual and the value is another dictionary containing their
    information. Each of these inner dictionaries should have the keys
    "birthday", "email", and "phone". In the case of missing data, map the key
    to None.

    Returns:
        (dict): a dictionary mapping names to a dictionary of personal info.
    """
    with open(filename, "r") as file:
        # Clean up the dates
        data = re.sub(r"(\s)(\d/)", r"\g<1>0\g<2>", file.read())
    data = re.sub(r"(/)(\d/)", r"\g<1>0\g<2>", data)
    data = re.sub(r"(/)(\d{2}\s)", r"\g<1>20\g<2>", data)

    # Clean up the phone numbers
    data = re.sub(r"(\s)(1-)", r"\1", data)
    data = re.sub(r"(\s\(?\d{3}\)?)(-)", r"\1", data)
    data = re.sub(r"(\s)(\d{3})(\d)", r"\1(\2)\3", data)

    # Parse the contacts
    contact_line = re.compile(r"(.*(?:\d|com|edu|net|org))")
    contacts_unparsed = contact_line.findall(data)

    # Parse the name, bday, number and email into a dictionary
    contacts = {}
    name = re.compile(r"([a-zA-Z]*(?: [a-zA-Z]*.?)? [a-zA-Z]*) ")
    number = re.compile(r"(\(\d{3}\)\d{3}-\d{4})")
    date = re.compile(r"(\d{1,2}/\d{1,2}/\d{1,4})")
    email = re.compile(r"(\S+@\S+)")
    for contact in contacts_unparsed:
        cname = name.findall(contact)
        # If any fields are empty, use None
        bday = date.findall(contact)
        if len(bday) == 0:
            bday = [None]
        cemail = email.findall(contact)
        if len(cemail) == 0:
            cemail = [None]
        cnum = number.findall(contact)
        if len(cnum) == 0:
            cnum = [None]
        # Add new contact to the dictionary
        contacts[cname[0]] = {"birthday": bday[0], "email": cemail[0], "phone": cnum[0]}
    # Return the dictionary of contacts
    return contacts





def test_prob2():
    pattern = prob2()
    print(bool(pattern.match(r"^{@}(?)[%]{.}(*)[_]{&}$")))

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

def test_prob4():
    pattern = prob4()
    matches = ["Mouse", "compile", "_123456789", "__x__", "while", 
        "max=4.2", "string= ''", "num_guesses"]
    non_matches = ["3rats", "err*r", "sq(x)", "sleep()", " x",
        "300", "is_4=(value==4)", "pattern = r'^one|two fish$'"]
    print("Matches: \n")
    for match in matches:
        print(bool(pattern.match(match)))
    print("\nNon Matches: \n")
    for non_match in non_matches:
        print(bool(pattern.match(non_match)))

def test_prob5():
    code = """
    k, i, p = 999, 1, 0 
    while k > i
        i *= 2 
        p += 1 
        if k != 999
            print("k should not have changed") 
        else
            pass
    print(p) 
    """
    prob5(code)

def prob5_trial():
    text = """
    k, i, p = 999, 1, 0
    while k > i
    """
    print(re.sub(r"(while.*)", r"\1:", text))

def prob6_trial():
    name = re.compile(r"(([A-Z]|[a-z])* ([A-Z]|[a-z])*. ?([A-Z]|[a-z])*)")
    number = re.compile(r"\d?-?\(?\d{3}\)?-?\d{3}-?\d{4}")
    date = re.compile(r"\d{1,2}/\d{1,2}/\d{1,4}")
    email = re.compile(r"\S+@\S+")
    email = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    all = re.compile(r"([a-zA-Z]* [a-zA-Z]*. [a-zA-Z]*) ((?:\d-)?\d{3}-\d{3}-\d{4}) (\d{1,2}/\d{1,2}/\d{1,4}) (\w.*@.*(?:com|net|org|edu))")

    print(bool(email.match("happy@gmail.net")))
    print(bool(date.match("1/19/2001")))
    print(bool(number.match("1-(541)-456-4758")))
    print(bool(name.match("Jane C. Frost")))
    print(all.findall("Jane C. Frost 1-(541)-456-4758 1/19/2001 happy@gmail.com"))
    print(number.findall("Jane C. Frost (541)-456-4758 1/19/2001 happy@gmail.com"))
    print(date.findall("Jane C. Frost (541)-456-4758 1/19/2001 happy@gmail.com"))
    print(email.findall("Jane C. Frost (541)-456-4758 1/19/2001 happy@gmail.com "))
    
