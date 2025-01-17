# classify.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018
# Extended by Daniel Gonzales (dsgonza2@illinois.edu) on 3/11/2018

import numpy as np
import math as math
"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.

train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
            This can be thought of as a list of 7500 vectors that are each
            3072 dimensional.  We have 3072 dimensions because there are
            each image is 32x32 and we have 3 color channels.
            So 32*32*3 = 3072. RGB values have been scaled to range 0-1.

train_labels - List of labels corresponding with images in train_set
example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
         and X1 is a picture of a dog and X2 is a picture of an airplane.
         Then train_labels := [1,0] because X1 contains a picture of an animal
         and X2 contains no animals in the picture.

dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
          It is the same format as train_set
"""

def trainPerceptron(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained weight and bias parameters
    features = len(train_set[0])
    w = np.zeros(features)
    b=0 #init weights and biases to zero
    num_token=0

    for i in range(max_iter):

        for y_iter,x in zip(train_labels,train_set):
            y = int(y_iter)
            if(y ==0):
                y=-1

            y_prime = np.sign(np.dot(w, x) + b)
            if (y != y_prime):
                w = w + learning_rate*y*x
                b = b + learning_rate*y*1

    return w, b

def classifyPerceptron(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train perceptron model and return predicted labels of development set
    w,b = trainPerceptron(train_set,train_labels,learning_rate,max_iter)
    result =[]
    for x in dev_set:
        y_prime = np.sign(np.dot(w, x) + b)
        if(y_prime > 0):
            result.append(1)
        else:
            result.append(0)
    return result

def sigmoid(x):
    # TODO: Write your code here
    # return output of sigmoid function given input x
    return 1 / (1+np.exp(-x))

def trainLR(train_set, train_labels, learning_rate, max_iter):
    # TODO: Write your code here
    # return the trained weight and bias parameters
    features = len(train_set[0])
    w = np.zeros(features)
    b=0                 #init weights and biases to zero

    for i in range(max_iter):
        gdw=0
        gdb=0
        N=0

        for y_iter,x in zip(train_labels,train_set):
            y = int(y_iter)
            N +=1
            y_prime = sigmoid(np.dot(w, x) + b)
            gdw -= (y_prime -y)*x
            gdb -= (y_prime -y)*1

        w = w + learning_rate*gdw/N
        b = b + learning_rate*gdb/N

    print("w",w)
    print("b",b)
    return w, b


def classifyLR(train_set, train_labels, dev_set, learning_rate, max_iter):
    # TODO: Write your code here
    # Train LR model and return predicted labels of development set
        w,b = trainLR(train_set,train_labels,learning_rate,max_iter)
        #print("w:",w , "b: ",b)
        result =[]
        for x in dev_set:
            y_prime = sigmoid(np.dot(w, x) + b)
            #print("yp:", y_prime)
            if(np.round(y_prime) >= 0.5):
                result.append(1)
            else:
                result.append(0)
        return result

def classifyEC(train_set, train_labels, dev_set, k):
    # Write your code here if you would like to attempt the extra credit
    return []
