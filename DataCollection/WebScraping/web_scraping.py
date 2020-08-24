"""Volume 3: Web Scraping.
Kameron Lightheart
MATH 403
9/16/2019
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from matplotlib import pyplot as plt

# Problem 1
def prob1():
    # Get source from example.com
    response = requests.get("http://www.example.com")
    
    # Write the source to a new example.html file
    with open("example.html", "w") as file:
        file.write(response.text)
        
    return response
    
# Problem 2
def prob2():
    """Examine the source code of http://www.example.com. Determine the names
    of the tags in the code and the value of the 'type' attribute associated
    with the 'style' tag.

    Returns:
        (set): A set of strings, each of which is the name of a tag.
        (str): The value of the 'type' attribute in the 'style' tag.
    """
    # Open file
    soup = None
    with open("example.html", "r") as file:
        soup = BeautifulSoup(file)

    # Generate set of all tag names
    tags = { tag.name for tag in soup.find_all() }

    # Get the style tag
    style_attrs = soup.find('style').attrs
    return tags, style_attrs["type"]


# Problem 3
def prob3(code):
    """Return a list of the names of the tags in the given HTML code."""
    # Load code into Beautiful Soup
    soup = BeautifulSoup(code)
    # Generate list of all the tag names
    tags = [ tag.name for tag in soup.find_all() ]
    return tags


# Problem 4
def prob4(filename="example.html"):
    """Read the specified file and load it into BeautifulSoup. Find the only
    <a> tag with a hyperlink and return its text.
    """
    html_soup = BeautifulSoup(prob1().text)
    a_href = html_soup.find("a", attrs={"href": True})
    return a_href.text


# Problem 5
def prob5(filename="san_diego_weather.html"):
    """Read the specified file and load it into BeautifulSoup. Return a list
    of the following tags:

    1. The tag containing the date 'Thursday, January 1, 2015'.
    2. The tags which contain the links 'Previous Day' and 'Next Day'.
    3. The tag which contains the number associated with the Actual Max
        Temperature.

    Returns:
        (list) A list of bs4.element.Tag objects (NOT text).
    """
    # Open file
    soup = None
    with open(filename, "r") as file:
        soup = BeautifulSoup(file)
    return_list = []
    # Get the tag with specified date in body
    return_list.append(soup.find(string="Thursday, January 1, 2015").parent)

    # Use regex to get both tags with Previous Day and Next Day
    tags_2 = soup.find_all(string=re.compile(r"(Previous Day|Next Day)"))
    return_list.append([tag.parent for tag in tags_2])
    
    # Find the max temperature attribute
    parent = soup.find(string="Max Temperature").parent.parent.parent
    child = parent.find("span", {"class": "wx-value"})
    return_list.append(child)
    
    return return_list


# Problem 6
def prob6(filename="large_banks_index.html"):
    """Read the specified file and load it into BeautifulSoup. Return a list
    of the tags containing the links to bank data from September 30, 2003 to
    December 31, 2014, where the dates are in reverse chronological order.

    Returns:
        (list): A list of bs4.element.Tag objects (NOT text).
    """
    # Open data
    soup = None
    with open(filename, "r") as file:
        soup = BeautifulSoup(file)
    # Get all the dates (already sorted)
    dates = soup.find_all("a", string=re.compile(r"[A-z]+ [0-9]+, [0-9]+"))
    return dates[1:]


# Problem 7
def prob(filename="large_banks_data.html"):
    """Read the specified file and load it into BeautifulSoup. Create a single
    figure with two subplots:

    1. A sorted bar chart of the seven banks with the most domestic branches.
    2. A sorted bar chart of the seven banks with the most foreign branches.

    In the case of a tie, sort the banks alphabetically by name.
    """
    # Open file
    soup = None
    with open(filename, "r") as file:
        soup = BeautifulSoup(file)
    # Get the table of bank info
    table = soup.find("table", {"cellpadding": "7"})

    # Load pandas data structure
    df = pd.read_html(str(table))[0]
    fig, axes = plt.subplots(2,1)

    df1 = df.copy()
    df1["Domestic Branches"] = pd.to_numeric(df1["Domestic Branches"], errors="coerce")
    domestic = df1.sort_values(["Domestic Branches"], ascending=False)[:7]
    domestic["Domestic Branches"] = domestic["Domestic Branches"].astype(float)
    domestic.plot.barh(y="Domestic Branches", x="Bank Name / Holding Co Name" 
                    , title="Top Seven Banks by Domestic Branches", ax=axes[0])

    df["Foreign Branches"] = pd.to_numeric(df["Foreign Branches"], errors="coerce")
    foreign = df.sort_values(["Foreign Branches"], ascending=False)[:7]
    foreign.plot.barh(y="Foreign Branches", x="Bank Name / Holding Co Name"
                    , title="Top Seven Banks by Foreign Branches", ax=axes[1])

    plt.subplots_adjust(left=0.25)
    plt.show()
    
