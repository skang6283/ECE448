# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019

"""
You should only modify code within this file for part 1 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class NeuralNet(torch.nn.Module):
    def __init__(self, lrate,loss_fn,in_size,out_size):
        """
        Initialize the layers of your neural network
        @param lrate: The learning rate for the model.
        @param loss_fn: The loss function
        @param in_size: Dimension of input
        @param out_size: Dimension of output
        The network should have the following architecture (in terms of hidden units):
        in_size -> 128 ->  out_size
        """
        super(NeuralNet, self).__init__()       # running the init for nn. module
        self.loss_fn = loss_fn
        self.lrate = lrate
        self.loss_fn = loss_fn
        self.in_size = in_size
        self.out_size= out_size

        # 28 * 28 in_size
        self.fc1 = nn.Linear(in_size, 128)      # fc = fully connected
        self.fc2 = nn.Linear(128,128)
        self.fc3 = nn.Linear(128,out_size)

        self.optimizer = optim.Adam(self.parameters(), lr = 0.001)

    def get_parameters(self):
        """ Get the parameters of your network
        @return params: a list of tensors containing all parameters of the network
        """


        return self.parameters()


    def forward(self, x):
        """ A forward pass of your autoencoder
        @param x: an (N, in_size) torch tensor
        @return y: an (N, out_size) torch tensor of output from the network
        """

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)

        #   return F.log_softmax(x, dim=1) ??

        return x

    def step(self, x,y):
        """
        Performs one gradient step through a batch of data x with labels y
        @param x: an (N, in_size) torch tensor
        @param y: an (N,) torch tensor
        @return L: total empirical risk (mean of losses) at this time step as a float
        """

        # forward + backward + optimize
        self.optimizer.zero_grad()
        L = self.loss_fn(self.forward(x), y)
        L.backward()
        self.optimizer.step()     # updates the parameters

        return L.item()

def fit(train_set,train_labels,dev_set,n_iter,batch_size=100):
    """ Fit a neural net.  Use the full batch size.
    @param train_set: an (N, out_size) torch tensor
    @param train_labels: an (N,) torch tensor
    @param dev_set: an (M, out_size) torch tensor
    @param n_iter: int, the number of batches to go through during training (not epoches)
                   when n_iter is small, only part of train_set will be used, which is OK,
                   meant to reduce runtime on autograder.
    @param batch_size: The size of each batch to train on.
    # return all of these:
    @return losses: list of total loss (as type float) at the beginning and after each iteration. Ensure len(losses) == n_iter
    @return yhats: an (M,) NumPy array of approximations to labels for dev_set
    @return net: A NeuralNet object
    # NOTE: This must work for arbitrary M and N
    """

    print("len:",len(train_set))
    print("len0:",len(train_set[0]))
    print("len1:",len(train_set[1]))


    loss=[]
    criterion = nn.CrossEntropyLoss()
    net = NeuralNet(0.00001, criterion, len(train_set[0]), 3) # cloth, shoe, bag

    mean = torch.mean(train_set,dim=-2,keepdim=True)
    std = torch.std(train_set,dim=-2,keepdim=True)

    #print("mean: ", mean)
    #print("Std: ",std)

    batch_num = len(train_set)
    for i in range(n_iter):
            begin = i*batch_size%(batch_num)
            end = (i+1)*batch_size%(batch_num+1)

            input_batch = train_set[begin:end]
            input_labels = train_labels[begin:end]
            # print("begin:", begin)
            # print("end:", end)
            # print("input batch",input_batch)
            # print("input label",input_labels)
            loss.append(net.step(input_batch, input_labels))
            #print("losses:",losses)


    dev_output = net(dev_set)
    #print(dev_output)
    #print(len(dev_set[0]))
    yhat =[]
    for idx, i in enumerate(dev_output):
        yhat.append(torch.argmax(i))
    yhats = np.array(yhat)
    losses = np.array(loss)

    print("yhat:",yhats)
    print("losssss: ",losses)


    return losses,yhats, net
