# nearest_neighbor.py
"""Volume 2: Nearest Neighbor Search.
Kameron Lightheart
MATH 321 Section 2
10/18/18
"""

import numpy as np
from scipy import linalg as la
from scipy.spatial import KDTree as kd
from scipy import stats

# Problem 1
def exhaustive_search(X, z):
    """Solve the nearest neighbor search problem with an exhaustive search.

    Parameters:
        X ((m,k) ndarray): a training set of m k-dimensional points.
        z ((k, ) ndarray): a k-dimensional target point.

    Returns:
        ((k,) ndarray) the element (row) of X that is nearest to z.
        (float) The Euclidean distance from the nearest neighbor to z.
    """
    #initialize shortest path and distance to the first row
    d_star = la.norm(z - X[0])
    x_star = X[0]
    #check the distance from each row of X and if shortest thus far, save it
    for i in range(X.shape[0]):
        #calculate distance from current row to target z
        x = X[i,:]
        cur_dist = la.norm(x - z)
        #if the distance is smallest thus far, save the row and distance
        if cur_dist < d_star:
            x_star = x
            d_star = cur_dist
    return x_star, d_star

# Problem 2: Write a KDTNode class.
class KDTNode:
    """A node class for K-D trees. Contains a value, a
    reference to the parent node, and references to two child nodes.
    """
    def __init__(self, data):
        """Construct a new node and set the value attribute. The other
        attributes will be set when the node is added to a tree.
        """
        if type(data) != np.ndarray:
            raise TypeError("Node input not a numpy array!!!")
        self.value = data
        self.left = None
        self.right = None
        self.pivot = None

# Problems 3 and 4
class KDT:
    """A k-dimensional binary tree for solving the nearest neighbor problem.

    Attributes:
        root (KDTNode): the root node of the tree. Like all other nodes in
            the tree, the root has a NumPy array of shape (k,) as its value.
        k (int): the dimension of the data in the tree.
    """
    def __init__(self):
        """Initialize the root and k attributes."""
        self.root = None
        self.k = None

    def find(self, data):
        """Return the node containing the data. If there is no such node in
        the tree, or if the tree is empty, raise a ValueError.
        """
        def _step(current):
            """Recursively step through the tree until finding the node
            containing the data. If there is no such node, raise a ValueError.
            """
            if current is None:                     # Base case 1: dead end.
                raise ValueError(str(data) + " is not in the tree")
            elif np.allclose(data, current.value):
                return current                      # Base case 2: data found!
            elif data[current.pivot] < current.value[current.pivot]:
                return _step(current.left)          # Recursively search left.
            else:
                return _step(current.right)         # Recursively search right.

        # Start the recursive search at the root of the tree.
        return _step(self.root)

    # Problem 3
    def insert(self, data):
        """Insert a new node containing the specified data.

        Parameters:
            data ((k,) ndarray): a k-dimensional point to insert into the tree.

        Raises:
            ValueError: if data does not have the same dimensions as other
                values in the tree.
        """
        def find_parent(current):
            """Recursively step through the tree until finding the node
            that should be the parent of node to be inserted.
            If there is no such node, raise a ValueError.
            """
            if np.allclose(data, current.value):
                raise ValueError("Duplicate data, cannot insert!!!")
            elif data[current.pivot] < current.value[current.pivot]:
                if current.left is None:
                    # Base case 1 Found parent! Child goes to the left
                    if current.pivot == self.k - 1:
                        #If pivot is at end of dimension, start over at 0
                        new_node.pivot = 0
                    else:
                        new_node.pivot = current.pivot + 1
                    #Set parents left child to the new node
                    current.left = new_node
                else:
                    return find_parent(current.left)  # Recursively search left.
            else:
                if current.right is None:
                    # Base case 2 Found Parent! Child goes to right
                    if current.pivot == self.k - 1:
                        #If pivot is at end of dimension, start over at 0
                        new_node.pivot = 0
                    else:
                        new_node.pivot = current.pivot + 1
                    #Set parents right child to the new node
                    current.right = new_node
                else:
                    return find_parent(current.right) # Recursively search right.
        new_node = KDTNode(data)
        if self.root == None:
            new_node.pivot = 0
            self.root = new_node
            self.k = len(data)
        elif len(data) != self.k:
            raise ValueError("Data is not k-dimensional!!!")
        else:
            find_parent(self.root)



    # Problem 4
    def query(self, z):
        """Find the value in the tree that is nearest to z.

        Parameters:
            z ((k,) ndarray): a k-dimensional target point.

        Returns:
            ((k,) ndarray) the value in the tree that is nearest to z.
            (float) The Euclidean distance from the nearest neighbor to z.
        """
        def KDSearch(current, nearest, d_star):
            """Recurse through the tree as if searching for target z.

            Parameters:
                current (KDTNode): the node we are currently examining.
                nearest (KDTNode): the closest known node to z.
                d_star  (int):     the distance from nearest to target.
            Returns:
                nearest (KDTNode): the node closest to the target z.
                d_star  (int):     the distance from nearest to target.
            """
            #Base case: dead end.
            if current is None:
                return nearest, d_star
            #set x to location of node we are examining
            x = current.value
            #set i to the pivot of node we are examining
            i = current.pivot
            #distance from x to z
            d_x_z = la.norm(x - z)
            #check if current is closer to z than nearest
            if d_x_z < d_star:
                nearest = current
                d_star = d_x_z
            #Search to the left
            if z[i] < x[i]:
                nearest, d_star = KDSearch(current.left, nearest, d_star)
                #Search to the right if needed
                if (z[i] + d_star) >= x[i]:
                    nearest, d_star = KDSearch(current.right, nearest, d_star)
            #Search to the right
            else:
                nearest, d_star = KDSearch(current.right, nearest, d_star)
                #Search to the left if needed
                if (z[i] - d_star) <= x[i]:
                    nearest, d_star = KDSearch(current.left, nearest, d_star)
            return nearest, d_star
        #If tree is empty, raise error
        if (self.root == None):
            raise ValueError("Tree is empty!!!")
        nearest, d_star = KDSearch(self.root, self.root, la.norm(self.root.value - z))
        return nearest.value, d_star



    def __str__(self):
        """String representation: a hierarchical list of nodes and their axes.

        Example:                           'KDT(k=2)
                    [5,5]                   [5 5]   pivot = 0
                    /   \                   [3 2]   pivot = 1
                [3,2]   [8,4]               [8 4]   pivot = 1
                    \       \               [2 6]   pivot = 0
                    [2,6]   [7,5]           [7 5]   pivot = 0'
        """
        if self.root is None:
            return "Empty KDT"
        nodes, strs = [self.root], []
        while nodes:
            current = nodes.pop(0)
            strs.append("{}\tpivot = {}".format(current.value, current.pivot))
            for child in [current.left, current.right]:
                if child:
                    nodes.append(child)
        return "KDT(k={})\n".format(self.k) + "\n".join(strs)


# Problem 5: Write a KNeighborsClassifier class.
class KNeighborsClassifier:
    """A class similar to KDTree but uses k nearest neighbors to vote and
        decide on what to label new elements as. Application of machine learning
    Attributes:
        root (KDTNode): the root node of the tree. Like all other nodes in
            the tree, the root has a NumPy array of shape (k,) as its value.
        k (int): the dimension of the data in the tree.
    """
    def __init__(self, n_neighbors):
        self.k = n_neighbors
        self.tree = None
        self.labels = None

    def fit(self, X, y):
        """ A loads the data in X into a KDTree tree
        Parameters:
            X (MxK Numpy Array): data to analyze
            y (1 dimentional Numpy array with M entries)
        """
        #Initialize the tree with the given data
        tree = kd(X)
        self.tree = tree
        self.labels = y

    def predict(self, z):
        """Makes predictions based on given data of what to label
        Parameters:
            z (1-dim Numpy array with k entries):
        Return
        """
        k_nearest_to_z, indicies = self.tree.query(z, self.k)
        return stats.mode(self.labels[indicies])[0][0]

# Problem 6
def prob6(n_neighbors, filename="mnist_subset.npz"):
    """Extract the data from the given file. Load a KNeighborsClassifier with
    the training data and the corresponding labels. Use the classifier to
    predict labels for the test data. Return the classification accuracy, the
    percentage of predictions that match the test labels.

    Parameters:
        n_neighbors (int): the number of neighbors to use for classification.
        filename (str): the name of the data file. Should be an npz file with
            keys 'X_train', 'y_train', 'X_test', and 'y_test'.

    Returns:
        (float): the classification accuracy.
    """
    #Extract the data
    data = np.load("mnist_subset.npz")
    X_train = data["X_train"].astype(np.float)
    y_train = data["y_train"]
    X_test = data["X_test"].astype(np.float)
    y_test = data["y_test"]

    # instantiate a KNeighborsClassifier to hold the data to make predictions
    myClassifier = KNeighborsClassifier(n_neighbors)
    myClassifier.fit(X_train, y_train)
    accurate_trains = 0
    prediction = 0
    # test each label
    for i in range(len(X_test)):
        target = X_test[i]
        #make prediction
        prediction = myClassifier.predict(target)
        # check accuracy
        if prediction == y_test[i]:
            accurate_trains += 1
    # return the accuracy ratio
    return accurate_trains / len(y_test)



if __name__ == "__main__":
    A = KDT()
    A.insert(np.array([5,5]))
    A.insert(np.array([3,2]))
    A.insert(np.array([2,6]))
    A.insert(np.array([8,4]))
    A.insert(np.array([7,7]))
    print(A.query(np.array([3,2.75])))
