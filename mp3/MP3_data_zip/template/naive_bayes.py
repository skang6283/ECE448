# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
# Modified by Jaewook Yeom 02/02/2020

"""
This is the main entry point for Part 1 of MP3. You should only modify code
within this file for Part 1 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as numpy
import math
from collections import Counter


def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter you provided with --laplace (1.0 by default)

    pos_prior - positive prior probability (between 0 and 1)
    """

    # TODO: Write your code here

    #Training Phase
    negative_data_count = {}
    positive_data_count = {}

    for i in range(len(train_set)):
        current_list = train_set[i]
        for each_word in current_list:
            #print(str.encode(each_word));
            if train_labels[i] == 0:
                if each_word not in negative_data_count:
                    negative_data_count[each_word] = 1
                else:
                    negative_data_count[each_word] +=1
            else:
                if each_word not in positive_data_count:
                    positive_data_count[each_word] = 1
                else:
                    positive_data_count[each_word] +=1

    negative_total = sum(negative_data_count.values())
    #print("negatve:", negative_total)
    positive_total = sum(positive_data_count.values())
    #print("positive:", positive_total)

    pwn = {} # P(Word=tiger|Type=Negative)
    pwp = {} # P(Word=tiger|Type=Positive)
    # P(Word=tiger|Type=Positive) =
    #  (# times 'tiger' appears in positive train set) / (# total words in positive train set including repeated words)

    for key in negative_data_count:
        pwn[key] = negative_data_count[key] / negative_total;
    for key in positive_data_count:
        pwp[key] = positive_data_count[key] / positive_total;

    total = negative_total + positive_total

    #development Phase


    result = []
    #Likelihood= count(x)+k / N+k|X|
    for dev_list in dev_set:
        pnw = 0;# P(Type = Negative |Words)
        ppw = 0;# P(Type = Positive |Words)
        for each_word in dev_list:
            if each_word in negative_data_count:
                likelihood = (negative_data_count[each_word] + smoothing_parameter) / (negative_total+smoothing_parameter* len(negative_data_count))
            else:
                likelihood =  smoothing_parameter / (negative_total + smoothing_parameter*len(negative_data_count))

            pnw += numpy.log10(likelihood)

            if each_word in positive_data_count:
                likelihood = (positive_data_count[each_word] + smoothing_parameter) / (positive_total+smoothing_parameter*len(positive_data_count))
            else:
                likelihood = smoothing_parameter / (positive_total + smoothing_parameter*len(positive_data_count))

            ppw += numpy.log10(likelihood)



        #print(pnw,"",ppw)
        if pnw < ppw:
            result.append(1)
        else:
            result.append(0)

    print(result)

    # return predicted labels of development set (make sure it's a list, not a numpy array or similar)
    return result
