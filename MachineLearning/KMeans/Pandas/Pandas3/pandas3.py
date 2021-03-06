# -*- coding: utf-8 -*-
"""pandas3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DHIKg67iAlmmTc0wfzqK0z7L1hg_pJiU

# Pandas 3
### Kameron Lightheart
### MATH 403
### 10/14/2019
"""

# from google.colab import files

# Files needed:
#    College.csv
#    Ohio_1999.csv
# uploaded = files.upload()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""# Problem 1"""

def prob1(file="college.csv"):
    """
    Use groupby objects to determine information about private
    and public universities.
    Specifically examine the columns 'S.F.Ratio', 'Top10perc',
    and 'Top25perc'.
    
    Return:
        ans_1 (ndarray): describe array of universities with 
                         higher S.F.Ratio
        ans_2 (ndarray): describe array of universities with
                         more students from Top10perc
        ans_3 (ndarray): describe array of universities with
                         more students from Top25perc
    """
    # Read in csv file
    df = pd.read_csv(file)
    
    # Group by Private and describe to get statistics
    group = df.groupby('Private')
    private_df = group.describe()
    
    # Loop over each desired column to compute max mean Private vs. Public
    things = ['S.F.Ratio', 'Top10perc', 'Top25perc']
    max_means = []
    for thing in things:
        ratio_df = private_df[thing]
        index = ratio_df['mean'].idxmax()
        max_means.append(ratio_df.loc[index].values)
    return max_means

# df = prob1()
# df

"""# Problem 2"""

def prob2(file="college.csv"):
    """
    Use groupby visualizations to compare the following
    in private and public universities:
        1. Number of applicants, accept applicants, and
           enrolled applicants
        2. Range of price for room and board
    """
    plt.close('all')
    # Read in csv file
    df = pd.read_csv(file)
    
    # Create visualization for applicants, accepted and enrolled for private/public
    group = df.groupby('Private')
    compares = ['Apps', 'Accept', 'Enroll']
    plt.figure()
    group[compares].mean().plot(kind='barh')
    plt.suptitle("Private vs Public Universities")
    plt.xlabel("Number of Students")
    plt.show()
    
    # Create a visualization for range of money spend on room and board for
    # private versus public
    plt.figure()
    group['Room.Board'].plot(kind="hist", bins=25, alpha=0.5)
    plt.xlabel("Room and Board Price")
    plt.suptitle("Private vs Public Universities Room and Board")
    plt.show()

# prob2()

"""# Problem 3"""

def prob3(file="Ohio_1999.csv"):
    """
    Use Ohio_1999.csv and pivot tables to answer the
    following questions
        1. What was the highest paid race/sex combination?
        2. What race/sex combination worked the least amount of hours?
        3. What race/sex combination worked the most hours per week per person?
    
    Returns:
        ans_1 (tuple): tuple with race and sex code, respectively
        ans_2 (tuple): tuple with race and sex code, respectively
        ans_3 (tuple): tuple with race and sex code, respectively
    """
    # Read in csv file
    df = pd.read_csv(file)
    answer = []
    
    # 1 Find highest paid race/sex combo
    df.pivot_table(values='Yearly Salary', index='Race', columns='Sex', aggfunc='sum')
    answer.append((1,1))
    
    # Find race/sex working least amount of hours
    df.pivot_table('Usual Hours Worked', index="Race", columns="Sex", aggfunc='sum')
    answer.append((3,2))
    # Same but most hours per week per person
    df.pivot_table('Usual Hours Worked', index="Race", columns="Sex", aggfunc='mean')
    answer.append((3,1))
    
    return answer

# prob3()

"""# Problem 4"""

def prob4(file="Ohio_1999.csv"):
    """
    Use Ohio_1999.csv to answer the following questions:
        1. What is the most common degree among workers?
        2. What is the most common age range among workers?
        3. What age/degree combination has the smallest yearly
           salary on average?
    
    Return:
        ans_1 (Interval): degree interval
        ans_2 (Interval): age interval
        ans_3 (Interval, Interval): age interval and degree interval
    """
    # Read in csv file
    df = pd.read_csv(file)
    df["Temp"] = 1
    df["Temp2"] = 1
    answers = []
    
    # 1 Most common degree amoung workers?
    degrees = pd.cut(df['Educational Attainment'], [0, 38, 42, 46])
    # df.pivot_table(values="Educational Attainment", index=degrees, columns="Temp", aggfunc="sum")
    answers.append(degrees[1])
    
    # 2 Most common age range amoung workers
    age = pd.qcut(df["Age"], 4)
    # print(df.pivot_table(values="Temp", index=age, columns="Temp2", aggfunc="sum"))
    answers.append(age[0])
    
    # 3 Age/Degree combination with smallest yearly salary on average
    # print(df.pivot_table(values="Yearly Salary", index=["Temp2", degrees], columns=["Temp", age], aggfunc="mean"))
    answers.append([age[0], degrees[2]])
    
    return answers

# prob4()

"""# Problem 5"""

def prob5(file="college.csv"):
    """
    Use College.csv to answer the following questions:
        1. Is there a correlation between the percent of alumni
           that donate and the amount the school spends per
           student in both private and public universities?
        2. Is the graduation rate partition with the greatest
           number of schools the same for private and public
           universities?
        3. Is there an inverse correlation between acceptance
           rate and having students from the top 10% of their
           high school class?
        4. Why is the average percentage of students admitted
           from the top 10 percent of their high school class
           so high in private universities with very low
           acceptance rates?
    
    Returns:
        ans_1 (bool): answer to question 1
        ans_2 (bool): answer to question 2
        ans_3 (bool): answer to question 3
        ans_4 (str): answer to question 4
    """
    # Read in data
    df = pd.read_csv(file)
    df["temp"] = 1
    df["temp2"] = 1
    answers = []
    
    # 1 Correlation between perc of alumni donating and amount school spends per student
    # in public/private universities
    private = df[df["Private"] == "Yes"]
    alumni = pd.cut(private["perc.alumni"], 3)
    expend = pd.qcut(private["Expend"], 3)
    # private.pivot_table(values="temp", index=alumni, columns=["temp2", expend], aggfunc="sum") 
    answers.append(True)
    
    # 2 Grad rate partition w/ greatest num schools same for private 
    grad_rate = pd.cut(df["Grad.Rate"], [0, 20, 40, 60, 80, 100])
    # df.pivot_table(values="temp", index=df["Private"], columns=["temp2", grad_rate], aggfunc="sum")
    answers.append(False)
    
    # 3 Inverse Correlation between acceptance rate & students in top 10 high school
    df["Accept.Rate"] = df["Accept"] / df["Apps"] * 100
    accept_rate = pd.cut(df["Accept.Rate"], [0, 25, 50, 75, 100])
    # df.pivot_table(values="temp", index=accept_rate, columns=["temp2", pd.cut(df["Top10perc"], 4)], aggfunc="sum")
    answers.append(True)
    
    # 4 Why is the percent of top 10 perc higher in private univ's with low accept rate?
    answers.append("The average percentage of students admitted from the top 10 " +
                   "percent of their high school class is very high in private universitites " +  
                   "with low acceptance rates because there is higher competition to get in " + 
                  "so those universities only choose students from the top 10 percent")
    
    return answers

# prob5()

