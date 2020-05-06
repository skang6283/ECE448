from collections import defaultdict
import math

class node:
    def __init__(self,tag,prev,probability,word):
        self.tag = tag
        self.prev = prev
        self.probability =probability
        self.word = word

    def __str__(self):
        #return "TAG:" + str(self.tag) + "    prob: "+ str(self.probability) + "  prev: " + str(self.prev)
        return "  word: " + str(self.word) +"   tag:" + str(self.tag)

    def __lt__(self, other):
        return self.probability < other.probability

def extra(train,test):
    '''
    TODO: implement improved viterbi algorithm for extra credits.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
            test data (list of sentences, no tags on the words)
            E.g  [[word1,word2,...][word1,word2,...]]
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''
    tag_set,tag_count, num_of_tags = get_tag_num(train)
    data_count = get_data_num(train)

    hapax, hapax_set = find_hapax(train,tag_set)


    # How often does each tag occur at the start of a sentence?)
    initial = initial_p(train)

    # How often does tag tb follow tag ta?
    transition = transition_p(train,tag_count)

    # how often does tag t yield word w?
    emission = hapax_emission_p(train,tag_count,tag_set,hapax)

    predicts = []


    for sentence in test:
        num_of_words = len(sentence)
        trellis = populate_trellis(sentence,tag_set,emission);

        for i in range(len(sentence)):
            for j,cur_tag in enumerate(tag_set):
                probability={}
                maxx =-1
                for k,prev_tag in enumerate(tag_set):
                    t_pair = (cur_tag , prev_tag)

                    if(i ==0):
                        tra = get_initial(initial,cur_tag)
                    else:
                        tra = get_probs(transition,t_pair)

                    if (i == 0):
                        prev_emi = 1;
                    else:
                        prev_emi = trellis[k][i-1].probability

                    cur_emi = trellis[j][i].probability
                    probability[prev_tag] =  prev_emi* tra * cur_emi
                    if (probability[prev_tag] > maxx):
                        maxx = probability[prev_tag]
                        if(i != 0):
                            prev_node = trellis[k][i-1]


                the_pre_tag = max(probability, key = probability.get)
                trellis[j][i].probability = probability[the_pre_tag]
                if(i == 0):
                    trellis[j][i].prev = "start"
                else:
                    trellis[j][i].prev = prev_node


        maxx=-1

        for j in range(num_of_tags):
            if (trellis[j][num_of_words-1].probability > maxx):
                last_node = trellis[j][num_of_words-1]

                maxx = trellis[j][num_of_words-1].probability

        output=[]
        pair = (last_node.word, last_node.tag)
        output.append(pair)
        while(last_node.prev != "start"):
            last_node = last_node.prev
            pair = (last_node.word, last_node.tag)
            output.append(pair)

        output.reverse()
        predicts.append(output)



    return predicts


def populate_trellis(sentence,tag_set,emission):
    num_of_words = len(sentence)
    num_of_tags = len(tag_set)
    trellis = [[node('NONE',0, 'NONE','NONE') for i in range(num_of_words)] for j in range(num_of_tags)]
    for j,tag in enumerate(tag_set):
        for i,word in enumerate(sentence):
            pair = (word,tag)
            trellis[j][i].probability = get_emission(pair,emission)
            trellis[j][i].tag = tag
            trellis[j][i].word = word


    return trellis

def get_emission(pair,emission):

    if pair in emission:
        num = emission[pair]
    elif (pair[1]== 'ADV' and pair[0].endswith('ly')):
        num = emission['ly']
        #print("its ADV:", pair[0])
    else:
    #elif pair not in emission:
        num = emission[pair[1]]

    return num

def get_probs(transition,t_pair):

    if t_pair not in transition:
        tra = transition["UNK"]
    else:
        tra = transition[t_pair]

    return tra

def get_initial(initial,tag):

    if tag in initial:
        out = initial[tag]
    else:
        out = initial["UNK"]
    return out

def find_hapax(train,tag_set):
    hapax_set={}
    hapax_prob={}
    total_count =0
    hapax_prob['ly'] =0
    for tag in tag_set:
        hapax_prob[tag] = 0

    for sentence in train:
        for word,tag in sentence:
            pair = (word,tag)
            if (word.endswith('ly') and tag == 'ADV'):
                hapax_prob['ly'] +=1;
            if pair not in hapax_set:
                hapax_set[pair] =1
                hapax_prob[tag] += 1
                total_count +=1

    for tag in tag_set:
        hapax_prob[tag] /=total_count
    hapax_prob['ly'] /=total_count
    hapax_prob["UNK"] =1/total_count

    print(hapax_prob)
    #print(hapax_set)
    return hapax_prob, hapax_set


def get_data_num(train):
    data_set={}
    for sentence in train:
        for word, tag in sentence:
            if word not in data_set:
                data_set[word] = {tag:1}
            else:
                exisiting_tags = data_set.get(word)
                if tag not in exisiting_tags:
                    exisiting_tags[tag] =1
                else:
                    exisiting_tags[tag] +=1
    return data_set

def get_tag_num(train):
    tag_set={}
    tag_count =0;
    tags =[]
    for sentence in train:
        for word, tag in sentence:

            if tag not in tag_set:
                tags.append(tag)
                tag_count +=1
                tag_set[tag] =1
            else:
                tag_set[tag] +=1
    return tags,tag_set,tag_count

def initial_p(train):
    init_p ={}
    tag_count=0
    for sentence in train:
        first_tag = sentence[0][1]
        if first_tag not in init_p:
            init_p[first_tag] = 1
            tag_count+=1
        else:
            init_p[first_tag] += 1

    for key in init_p:
        init_p[key] = (init_p[key]+0.) /(len(train) + 0.000001*tag_count)
    init_p["UNK"] = 0.000001/(len(train) + 0.000001*tag_count)

    return init_p


def transition_p(train,tag_set):
    tp = {}

    for sentence in train:
        for i in range(1,len(sentence)):
            prev_tag = sentence[i-1][1]
            cur_tag = sentence[i][1]
            tag_tuple = (cur_tag,prev_tag)
            if tag_tuple not in tp:
                tp[tag_tuple] = 1
            else:
                tp[tag_tuple] += 1

    for key in tp:
        #tp[key] /= tag_set[key[1]]
        tp[key] = (tp[key]+0.000001)/(tag_set[key[1]] + 0.000001 * len(tp))

    tp["UNK"] = 0.000001/(sum(tp.values()) + 0.000001 * len(tp))

    return tp

def emission_p(train,tag_count,tag_set):
    emission = {}
    total_tag_count=0
    for sentence in train:
        for pair in sentence:
            if pair not in emission:
                emission[pair] = 1
            else:
                emission[pair] +=1

    for key in emission:
        #emission[key] /= tag_count[key[1]]
        emission[key] = (emission[key] + 0.000001) / (tag_count[key[1]]+0.000001*len(emission))

    for tag in tag_set:
        #emission[tag] = 0.000001/tag_count[tag]
        emission[tag] = 0.000001/(tag_count[tag]+0.000001*len(emission))

    return emission

def hapax_emission_p(train,tag_count,tag_set,hapax):
    emission = {}
    total_tag_count=0
    for sentence in train:
        for pair in sentence:
            if pair not in emission:
                emission[pair] = 1
            else:
                emission[pair] +=1

    # num_types ={}
    # for tag in tag_set:
    #     for word ,tag in emission:
    #         if tag not in num_types:
    #             num_types[tag] =1;
    #         else:
    #             num_types[tag] +1;



    for key in emission:
        #emission[key] /= tag_count[key[1]]
        emission[key] = (emission[key] + 0.000001) / (tag_count[key[1]]+0.000001*len(emission))

    for tag in tag_set:
        #emission[tag] = 0.000001/tag_count[tag]
        emission[tag] = (0.000001*hapax[tag])/(tag_count[tag]+0.000001*len(emission))
    emission['ly'] = (0.000001*hapax['ly'])/(tag_count[tag]+0.000001*len(emission))
    return emission
