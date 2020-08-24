# test_nearest_neighbor.py
"""
Volume 2: Nearest Neighbor (Test File)
Kameron Lightheart
MATH 321 Section 2
10/18/18
"""

import nearest_neighbor
import pytest
import numpy as np
from scipy import linalg as la


@pytest.fixture
def set_up_matricies_targets():
    z_3_0s = np.zeros((1, 3))
    z_3_9s = np.full((1, 3), 9)
    m_33_0s = np.zeros((3,3))
    m_33_3s = np.full((3, 3), 3)
    m_33_123 = np.array([[1,1,1],[2,2,2],[3,3,3]])
    m_33_neg145 = np.array([[-1,-1,-1],[4,4,4],[5,5,5]])


def test_exhaustive_search():
    #initialize some targets and some training set points
    z_3_0s, z_3_9s, m_33_0s,\
        m_33_3s, m_33_123, m_33_neg145 = set_up_matricies_targets()
    assert(exhaustive_search(m_33_0s, z_3_0s)) == np.zeros((1,3), 3), 0
    assert(exhaustive_search(m_33_9s, z_3_0s)) == np.full((1, 3), 9), la.norm(m_33_9s, z_3_0s)
