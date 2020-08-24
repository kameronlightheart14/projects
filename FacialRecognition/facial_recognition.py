# facial_recognition.py
"""
Kameron Lightheart
MATH 345 Section 2
11/27/18
"""

import os
import numpy as np
from imageio import imread
from matplotlib import pyplot as plt

def get_faces(path="./faces94"):
    """
    Traverse the directory and get one image per subdirectory.
    1See http://cswww.essex.ac.uk/mv/allfaces/faces94.html. 7374 Lab7.FacialRecognition
    """
    faces = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for fname in filenames:
            if fname[-3:]=="jpg":
            # Only get jpg images. # Load the image, convert it to grayscale,
            # and flatten it into a vector.
                faces.append(np.ravel(imread(dirpath+"/"+fname, as_gray=True)))
                break
        # Put all the face vectors column-wise into a matrix.
    return np.transpose(faces)

def prob1():
    def plot_image(flat_image, m, n):
        """
        This function takes in a image as a flat mn vector, converts it back
        to it's original size and plots the result
        Parameters:
            flat_image (np.array): flattened image array
            m, n (int, int) size of original array
        Returns:
            Nothing, plots the image
        """
        image = np.reshape(flat_image, (m, n))
        image = image / 255
        if len(image.shape) == 2:
            plt.imshow(image, cmap="gray")
        else:
            plt.imshow(image)
        plt.show()

    face_database = get_faces()
    plot_image(face_database[:,0], 200, 180)

class FacialRec:
    """Class for facial FacialRecognition"""

    def __init__(self, path="./faces94"):
        self.F = get_faces()
        k = (self.F.shape[1])
        vector_sum = np.zeros(k)
        for i in range(k):
            vector_sumself.F[:,i] for i in range(k)]
        self.mean = 1/k *
        #self.F_bar =
