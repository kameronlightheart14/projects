#!/usr/bin/python3

#from PyQt5.QtCore import QLineF, QPointF



import math
import time
import numpy as np

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1

class GeneSequencing:

    def __init__( self ):
        pass

# This is the method called by the GUI.  _sequences_ is a list of the ten sequences, _table_ is a
# handle to the GUI so it can be updated as you find results, _banded_ is a boolean that tells
# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you 
# how many base pairs to use in computing the alignment
    def align( self, sequences, table, banded, align_length ):
        self.banded = banded
        self.MaxCharactersToAlign = align_length
        results = []

        for i in range(len(sequences)):
            jresults = []
            for j in range(len(sequences)):
                if j < i:
                   s = {}
                else:
###################################################################################################
# your code should replace these three statements and populate the three variables: score, alignment1 and alignment2
                    str1, str2 = '-' + sequences[i], '-' + sequences[j]
                    if len(sequences[i]) > len(sequences[j]):
                        temp = str1
                        str1 = str2
                        str2 = temp
                    if banded:
                        score, alignment1, alignment2 = self.banded_path_dist('-' + sequences[i], '-' + sequences[j])
                    else:
                        score, alignment1, alignment2 = self.calc_path_dist('-' + sequences[i], '-' + sequences[j])

                    if i == 2 and j == 9:
                        print(alignment1)
                        print(alignment2)

                    # score = i + j
                    # alignment1 = 'abc-easy  DEBUG:(seq{}, {} chars,align_len={}{})'.format(i+1,
                    #     len(sequences[i]), align_length, ',BANDED' if banded else '')
                    # alignment2 = 'as-123--  DEBUG:(seq{}, {} chars,align_len={}{})'.format(j+1,
                    #     len(sequences[j]), align_length, ',BANDED' if banded else '')
###################################################################################################                    
                    s = {'align_cost':score, 'seqi_first100':alignment1, 'seqj_first100':alignment2}
                    table.item(i,j).setText('{}'.format(int(score) if score != math.inf else score))
                    table.repaint()    
                jresults.append(s)
            results.append(jresults)
        return results

    def calc_path_dist(self, str1, str2):
        m,n = len(str1), len(str2)
        if m-1 > self.MaxCharactersToAlign:
            m = self.MaxCharactersToAlign + 1
        if n-1 > self.MaxCharactersToAlign:
            n = self.MaxCharactersToAlign + 1
        E = np.empty((m,n))
        prev = np.empty((m,n))
        start = 1
        if str1[1] == str2[1]:
            start = -3
        E[:,0] = 0
        E[0,:] = 0
        E[1:,1] = np.arange(start, 5*(m-1)+start, 5)
        prev[1:,1] = np.ones(m-1)
        E[1,1:] = np.arange(start, 5*(n-1)+start, 5)
        prev[1,1:] = np.zeros(n-1)
        prev[1,1] = 2

        def diff(i,j):
            if str1[i] == str2[j]:
                return -3
            else:
                return 1
            
        for i in range(2, m):
            for j in range(2, n):
                temp = [E[i-1,j] + 5, E[i,j-1]+5, E[i-1,j-1]+diff(i,j)]
                index = np.argmin(temp)
                E[i,j] = temp[index]
                # index of 0,1,2 represents left, up and diagonal respectively
                prev[i,j] = index

        align1, align2 = [], []
        i,j = m-1,n-1
        while True:
            prev_val = prev[i,j]
            if i == 0:
                align1.append(str1[i])
                align2.append("-")
                j -= 1
            elif j == 0:
                align1.append("-")
                align2.append(str2[j])
                i -= 1
            elif prev_val == 0:
                align1.append("-")
                align2.append(str2[j])
                i -= 1
            elif prev_val == 1:
                align1.append(str1[i])
                align2.append("-")
                j -= 1
            else:
                align1.append(str1[i])
                align2.append(str2[j])
                i -= 1
                j -= 1
            
            if i == 0 and j == 0:
                break

        return E[-1,-1], ''.join(align1[::-1]), ''.join(align2[::-1]) 

    def banded_path_dist(self, str1, str2):
        m,n = len(str1), len(str2)
        if m-1 > self.MaxCharactersToAlign:
            m = self.MaxCharactersToAlign + 1
        if n-1 > self.MaxCharactersToAlign:
            n = self.MaxCharactersToAlign + 1
        E = np.zeros((m,n)) + np.inf
        prev = np.zeros((m,n))
        start = 1
        if str1[1] == str2[1]:
            start = -3
        E[1:,1] = np.arange(start, 5*(m-1)+start, 5)
        prev[1:,1] = np.ones(m-1)
        E[1,1:] = np.arange(start, 5*(n-1)+start, 5)
        prev[1,1:] = np.zeros(n-1)
        prev[1,1] = 2

        def diff(i,j):
            if str1[i] == str2[j]:
                return -3
            else:
                return 1
            
        for i in range(2, m):
            for j in range(i-3, i+4):
                if j < 2 or j >= n:
                    continue
                temp = [E[i-1,j] + 5, E[i,j-1]+5, E[i-1,j-1]+diff(i,j)]
                index = np.argmin(temp)
                E[i,j] = temp[index]
                # index of 0,1,2 represents left, up and diagonal respectively
                prev[i,j] = index

        if E[-1,-1] == np.inf:
            return np.inf, "No Alignment Possible", "No Alignment Possible"

        align1, align2 = [], []
        i,j = m-1,n-1
        while True:
            prev_val = prev[i,j]
            if i == 0:
                align1.append(str1[i])
                align2.append("-")
                j -= 1
            elif j == 0:
                align1.append("-")
                align2.append(str2[j])
                i -= 1
            elif prev_val == 0:
                align1.append("-")
                align2.append(str2[j])
                i -= 1
            elif prev_val == 1:
                align1.append(str1[i])
                align2.append("-")
                j -= 1
            else:
                align1.append(str1[i])
                align2.append(str2[j])
                i -= 1
                j -= 1
            
            if i == 0 and j == 0:
                break

        return E[-1,-1], ''.join(align1[::-1]), ''.join(align2[::-1]) 
