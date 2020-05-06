"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

def baseline(train, test):
    '''
    TODO: implement the baseline algorithm. This function has time out limitation of 1 minute.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
            test data (list of sentences, no tags on the words)
            E.g  [[word1,word2,...][word1,word2,...]]
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''

    # train - list of lists(sentences) of tuples
    # output - list of lists(sentences)


    data_set={}
    tag_set={}
    for sentence in train:
        for word, tag in sentence:

            if tag not in tag_set:
                tag_set[tag] =1;
            else:
                tag_set[tag] +=1;


            if word not in data_set:
                data_set[word] = {tag:1}
            else:
                exisiting_tags = data_set.get(word)
                if tag not in exisiting_tags:
                    exisiting_tags[tag] =1
                else:
                    exisiting_tags[tag] +=1
                data_set[word] = exisiting_tags

    most_seen_tag = max(tag_set, key = tag_set.get)
    print(most_seen_tag)

    predicts = []
    predicted_sentence =[]
    for sentence in test:
        predicted_sentence=[]
        for word in sentence:
            if word in data_set:
                tags = data_set[word]
                tag = max(tags, key = tags.get)
                predicted_tuple = (word, tag)
            else:
                predicted_tuple = (word, most_seen_tag)
            predicted_sentence.append(predicted_tuple)
        predicts.append(predicted_sentence)


    #print(predicts)
    return predicts



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


def viterbi_p1(train, test):
    '''
    TODO: implement the simple Viterbi algorithm. This function has time out limitation for 3 mins.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words)
            E.g [[word1,word2...]]
    output: list of sentences with tags on the words
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''


    # tag_set - # of occurrences for each tag
    # initial_p_set
    data_count = get_data_num(train)

    tag_set,tag_count, num_of_tags = get_tag_num(train)

    # How often does each tag occur at the start of a sentence?)
    initial = initial_p(train)

    # How often does tag tb follow tag ta?
    transition = transition_p(train,tag_count)

    # how often does tag t yield word w?
    emission = emission_p(train,tag_count,tag_set)

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

def viterbi_p2(train, test):
    '''
    TODO: implement the optimized Viterbi algorithm. This function has time out limitation for 3 mins.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words)
            E.g [[word1,word2...]]
    output: list of sentences with tags on the words
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''

    tag_set,tag_count, num_of_tags = get_tag_num(train)
    data_count = get_data_num(train)

    hapax = find_hapax(train,tag_set)


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

    if pair not in emission:
        num = emission[pair[1]]
    else:
        num = emission[pair]
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
    for tag in tag_set:
        hapax_prob[tag] = 0

    for sentence in train:
        for word,tag in sentence:
            pair = (word,tag)
            if pair not in hapax_set:
                hapax_set[pair] =1
                hapax_prob[tag] += 1
                total_count +=1

    for tag in tag_set:
        hapax_prob[tag] /=total_count
    hapax_prob["UNK"] =1/total_count

    print(hapax_prob)

    return hapax_prob


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
        init_p[key] = (init_p[key]+0.001) /(len(train) + 0.001*tag_count)
    init_p["UNK"] = 0.001/(len(train) + 0.001*tag_count)

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
        tp[key] = (tp[key]+0.00001)/(tag_set[key[1]] + 0.00001 * len(tp))

    tp["UNK"] = 0.00001/(sum(tp.values()) + 0.00001 * len(tp))

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
        emission[key] = (emission[key] + 0.00001) / (tag_count[key[1]]+0.00001*len(emission))

    for tag in tag_set:
        #emission[tag] = 0.000001/tag_count[tag]
        emission[tag] = 0.00001/(tag_count[tag]+0.00001*len(emission))

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

    for key in emission:
        #emission[key] /= tag_count[key[1]]
        emission[key] = (emission[key] + 0.00001) / (tag_count[key[1]]+0.00001*len(emission))

    for tag in tag_set:
        #emission[tag] = 0.000001/tag_count[tag]
        emission[tag] = (0.00001*hapax[tag])/(tag_count[tag]+0.00001*len(emission))

    return emission
