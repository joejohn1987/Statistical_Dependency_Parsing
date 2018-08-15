'''
Model.py provides functions to train, save, and load a model.
'''


import pickle
import feature
import parser
import numpy as np
import gzip
import random
import oracle
import eva


def save_model(model, path):
    stream = gzip.open(path, 'wb')
    pickle.dump(model, stream, -1)
    stream.close()

def load_model(path):
    stream = gzip.open(path, 'rb')
    model = pickle.load(stream)
    stream.close()
    return model

class model:
    def __init__(self, train_sentences, test_sentences, gold_sentences):
        print('Initiating the model')
        self.pos_dict = feature.build_pos_dict(train_sentences)
        self.feature_dict = feature.build_feature_dict(train_sentences)
        self.train_sentences = train_sentences
        self.test_sentences = test_sentences
        self.gold_sentences = gold_sentences
        self.weight = np.zeros((4,len(self.feature_dict)))
        self.weight_a = np.zeros((4,len(self.feature_dict)))
        self.weight_c = np.zeros((4,len(self.feature_dict)))

        print('---> done!')


    def train_model(self,iteration):
        print('start building model')
        print('=======================================')
        print('total number of iteration:',iteration)
        print('=======================================')


        steps = 0


        for i in range(iteration):
            random.shuffle(self.train_sentences)
            print('iteration:', i+1)
            for sentence in self.train_sentences:
                state = parser.State(sentence)
                gold_arcs = sentence.gold_arcs
                while not parser.is_terminal(state):
                    state_features_id = feature.feature_to_index(feature.feature_extraction(sentence, state), self.feature_dict)
                    state, transition = parser.oracle_parsing(state, gold_arcs)
                    arcs_scores = []
                    for i in range(4):
                        score = 0
                        for f in state_features_id:
                            score = score + self.weight[i,f]
                        arcs_scores.append(score)
                    sign_arcs_scores = [np.sign(n) for n in arcs_scores]

                    for i in range(4):
                        for f in state_features_id:
                            if i == transition and sign_arcs_scores[i]<1:
                                self.weight[i, f] = self.weight[i, f] + 1
                                self.weight_c[i, f] = self.weight_c[i, f] + steps

                            elif i != transition and sign_arcs_scores[i]==1:
                                self.weight[i, f] = self.weight[i, f] - 1
                                self.weight_c[i, f] = self.weight_c[i, f] - steps
                    steps = steps + 1


            self.weight_a = self.weight - ((1 / steps)*self.weight_c)
            self.parsing(self.test_sentences)
            UAS = eva.UAS(self.gold_sentences, self.test_sentences)
            print(UAS)
        print('---> finished building model!')


    def parsing(self, test_sentences):
        for sentence in test_sentences:
            state = parser.State(sentence)
            while not parser.is_terminal(state):
                state_features_id = feature.feature_to_index(feature.feature_extraction(sentence, state), self.feature_dict)
                arcs_scores = []
                valid_transition = oracle.valid_transition(state)
                for i in valid_transition:
                    score = 0
                    for f in state_features_id:
                        score = score + self.weight_a[i, f]
                    arcs_scores.append(score)
                transition = valid_transition[arcs_scores.index(max(arcs_scores))]
                state = parser.model_parsing(state, transition)
            sentence.head = parser.state2tree(state, sentence.head)



    def random_parsing(self, test_sentences):
        print('start random parsing')
        for sentence in test_sentences:
            state = parser.State(sentence)
            valid_transition = oracle.valid_transition(state)
            while not parser.is_terminal(state):
                transition = random.choice(valid_transition)
                state = parser.model_parsing(state, transition)
            sentence.head = parser.state2tree(state, sentence.head)
        print('---> random parsing done!')

    def labelling(self, test_sentences):
        for sentence in test_sentences:
