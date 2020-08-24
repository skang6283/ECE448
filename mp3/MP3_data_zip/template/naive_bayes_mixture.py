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
This is the main entry point for Part 2 of this MP. You should only modify code
within this file for Part 2 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


import numpy as numpy
import math
from collections import Counter





def naiveBayesMixture(train_set, train_labels, dev_set, bigram_lambda,unigram_smoothing_parameter, bigram_smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    bigram_lambda - float between 0 and 1

    unigram_smoothing_parameter - Laplace smoothing parameter for unigram model (between 0 and 1)

    bigram_smoothing_parameter - Laplace smoothing parameter for bigram model (between 0 and 1)

    pos_prior - positive prior probability (between 0 and 1)
    """



    negative_data_count= {}
    positive_data_count= {}


    bigram_list_list=[[i for i in range(len(train_set[i])-1)]  for i in range(len(train_set))]          #list of list of pair_list
    bigram_list=[]                            #list of pair_list

    # print(bigram_list_list[0])
    # print(bigram_list_list[1])
    # print(bigram_list_list[2])


    #bigram_list_list =[]
    for i in range(len(train_set)):
        current_list = train_set[i]
        bigram_list.clear()
        for j in range(len(current_list)-1):
            bigram_list.append(tuple(current_list[j:j+2]))
        #bigram_list_list.append(bigram_list)
        for k in range(len(bigram_list)):
            bigram_list_list[i][k]= bigram_list[k]
     #
     # print(bigram_list_list[0])
     # print(bigram_list_list[1])
     # print(bigram_list_list[2])



    for i in range(len(bigram_list_list)):
        current_list = bigram_list_list[i]
        # print(current_list)
        # print()
        for each_pair in current_list:
            if train_labels[i] == 0:
                if each_pair not in negative_data_count:
                    negative_data_count[each_pair] = 1
                else:
                    negative_data_count[each_pair] +=1
            else:
                if each_pair not in positive_data_count:
                    positive_data_count[each_pair] = 1
                else:
                    positive_data_count[each_pair] +=1

    # for a in negative_data_count:
    #     print(str.encode(a[0]), str.encode(a[1]), negative_data_count[a])


    #print(str.encode(positive_data_count))

    negative_total = sum(negative_data_count.values())
    print("negatve:", negative_total)
    positive_total = sum(positive_data_count.values())
    print("positive:", positive_total)

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

    dev_bigram_list=[[i for i in range(len(dev_set[i])-1)]  for i in range(len(dev_set))]
    for i in range(len(dev_set)):
        current_list = dev_set[i]             #word list
        bigram_list.clear()
        for j in range(len(current_list)-1):
            bigram_list.append(tuple(current_list[j:j+2]))
        for k in range(len(bigram_list)):
            dev_bigram_list[i][k]= bigram_list[k]


    uni_negative_data_count, uni_positive_data_count, uni_negative_total, uni_positive_total, uni_total = naiveBayes(train_set, train_labels)

    # for a in uni_negative_data_count:
    #     print(str.encode(a), uni_negative_data_count[a])

    result = []
    #Likelihood= count(x)+k / N+k|X|
    for dev_list in dev_bigram_list:
        bi_pnw = 0;# P(Type = Negative |Words)
        bi_ppw = 0;# P(Type = Positive |Words)
        uni_pnw = 0;
        uni_ppw = 0;
        count =0;

        for each_pair in dev_list:
            count +=1
            #print(str.encode(each_pair[0]),str.encode(each_pair[1]))
            #print(each_pair)
            if each_pair in negative_data_count:
                bi_likelihood = (negative_data_count[each_pair] + bigram_smoothing_parameter) / (negative_total+bigram_smoothing_parameter*len(negative_data_count))
            else:
                bi_likelihood =  bigram_smoothing_parameter / (negative_total + bigram_smoothing_parameter*(len(negative_data_count)+1))

            bi_pnw += numpy.log10(bi_likelihood)

            if each_pair in positive_data_count:
                bi_likelihood = (positive_data_count[each_pair] + bigram_smoothing_parameter) / (positive_total+bigram_smoothing_parameter*len(positive_data_count))
            else:
                bi_likelihood = bigram_smoothing_parameter / (positive_total + bigram_smoothing_parameter*(len(positive_data_count)+1))

            bi_ppw += numpy.log10(bi_likelihood)


            if each_pair[0] in uni_negative_data_count:
                uni_likelihood = (uni_negative_data_count[each_pair[0]] + unigram_smoothing_parameter) / (uni_negative_total+unigram_smoothing_parameter*len(uni_negative_data_count))
            else:
                uni_likelihood =  unigram_smoothing_parameter / (uni_negative_total + unigram_smoothing_parameter*(len(uni_negative_data_count)+1))

            uni_pnw += numpy.log10(uni_likelihood)

            if each_pair[0] in uni_positive_data_count:
                uni_likelihood = (uni_positive_data_count[each_pair[0]] + unigram_smoothing_parameter) / (uni_positive_total+unigram_smoothing_parameter*len(uni_positive_data_count))
            else:
                uni_likelihood = unigram_smoothing_parameter / (uni_positive_total + unigram_smoothing_parameter*(len(uni_positive_data_count)+1))
            uni_ppw += numpy.log10(uni_likelihood)

            if count == len(dev_list)-1:
                if each_pair[1] in uni_negative_data_count:
                    uni_likelihood = (uni_negative_data_count[each_pair[1]] + unigram_smoothing_parameter) / (uni_negative_total+unigram_smoothing_parameter*len(uni_negative_data_count))
                else:
                    uni_likelihood =  unigram_smoothing_parameter / (uni_negative_total + unigram_smoothing_parameter*(len(uni_negative_data_count)+1))

                uni_pnw += numpy.log10(uni_likelihood)

                if each_pair[1] in uni_positive_data_count:
                    uni_likelihood = (uni_positive_data_count[each_pair[1]] + unigram_smoothing_parameter) / (uni_positive_total+unigram_smoothing_parameter*len(uni_positive_data_count))
                else:
                    uni_likelihood = unigram_smoothing_parameter / (uni_positive_total + unigram_smoothing_parameter*(len(uni_positive_data_count)+1))
                uni_ppw += numpy.log10(uni_likelihood)



        total_pnw = (1-bigram_lambda)*uni_pnw + bigram_lambda * bi_pnw
        total_ppw = (1-bigram_lambda)*uni_ppw + bigram_lambda * bi_ppw
        #print(total_pnw,"", total_ppw)
        if total_pnw <= total_ppw:
            result.append(1)
        else:
            result.append(0)

    print(result)

    # return predicted labels of development set (make sure it's a list, not a numpy array or similar)
    return result


def naiveBayes(train_set, train_labels):
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

    #TODO: Write your code here

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

    total = negative_total + positive_total

    #development Phase



    return negative_data_count, positive_data_count, negative_total, positive_total, total
