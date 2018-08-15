'''
feature.py stores the feature templates and provides relative function
'''


import parser

def feature_extraction(sentence, state):
    #feature template
    features = []
    if len(state.buff) >= 1:
        #unigram
        b0form = 'b0form' + sentence.form[int(state.buff[0])]
        b0lemma = 'b0lemma' + sentence.lemma[int(state.buff[0])]
        b0cpos = 'b0cpos' + sentence.cpos[int(state.buff[0])]
        b0ld = 'b0ld' + get_ld(state.buff[0], state.arcs)
        s0form = 's0form' + sentence.form[int(state.stack[-1])]
        s0lemma = 's0lemma' + sentence.lemma[int(state.stack[-1])]
        s0cpos = 's0cpos' + sentence.cpos[int(state.stack[-1])]
        s0head = 's0head' + get_head(state.stack[-1], state.arcs)
        s0ld = 's0ld' + get_ld(state.stack[-1], state.arcs)
        s0rd = 's0rd' + get_rd(state.stack[-1], state.arcs)
        b0formcpos = b0form + b0cpos
        s0formcpos = s0form + s0cpos
        b0feats = 'b0feats' + sentence.feats[int(state.buff[0])]
        s0feats = 's0feats' + sentence.feats[int(state.stack[-1])]
        s0headcpos = 's0headcpos' + get_cpos(get_head(state.stack[-1], state.arcs), sentence)
        s0ldcpos = 's0ldcpos' + get_cpos(get_ld(state.stack[-1], state.arcs), sentence)
        s0rdcpos = 's0ldcpos' + get_cpos(get_rd(state.stack[-1], state.arcs), sentence)
        b0ldcpos = 'b0ldcpos' + get_cpos(get_ld(state.buff[0], state.arcs), sentence)

        # bigram
        s0formcpos_b0formpos = s0formcpos + b0formcpos
        s0formcpos_b0form = s0formcpos + b0form
        s0formpos_b0cpos = s0formcpos + b0cpos
        s0form_b0formpos = s0form + b0formcpos
        s0form_b0form = s0form + b0form
        s0form_b0cpos = s0form + b0cpos
        s0cpos_b0formcpos = s0cpos + b0formcpos
        s0cpos_b0form = s0cpos + b0form
        s0cpos_b0cpos = s0cpos + b0cpos

        # trigram
        s0headcpos_s0cpos_b0cpos = s0headcpos + s0cpos + b0cpos
        s0cpos_s0ldcpos_b0cops = s0cpos + s0ldcpos + b0cpos
        s0cpos_s0rdcpos_b0cpos = s0cpos + s0rdcpos + b0cpos
        s0cpos_b0cpos_b0ldcpos = s0cpos + b0cpos + b0ldcpos


        # Dummy
        # b1form = 'b1formdummy'
        # b1cpos = 'b1cposdummy'
        # b2form = 'b2formdummy'
        # b2cpos = 'b2cposdummy'

        features = features + [b0form,b0lemma,b0cpos,b0ld,s0form,s0lemma,s0cpos,s0head,s0ld,s0rd,b0feats,s0feats,s0ldcpos,s0rdcpos,b0ldcpos,
                               b0formcpos,s0formcpos,s0formcpos_b0formpos, s0formcpos_b0form, s0formpos_b0cpos,
                               s0form_b0formpos, s0form_b0form, s0form_b0cpos,s0cpos_b0formcpos, s0cpos_b0form, s0cpos_b0cpos,
                               s0headcpos_s0cpos_b0cpos,s0cpos_s0ldcpos_b0cops,s0cpos_s0rdcpos_b0cpos,s0cpos_b0cpos_b0ldcpos ]

    if len(state.buff) >= 2:
        # unigram
        b1form = 'b1form' + sentence.form[int(state.buff[1])]
        b1cpos = 'b1cpos' + sentence.cpos[int(state.buff[1])]
        b1feats = 'b1feats' + sentence.feats[int(state.buff[1])]
        b1formcpos = b1form + b1cpos
        # bigram
        b0cpos_b1cpos = b0cpos + b1cpos
        # trigram
        s0cpos_b0cpos_b1cpos = s0cpos + b0cpos + b1cpos

        features = features + [b1form, b1cpos, b1formcpos, b1feats, b0cpos_b1cpos,
                               b0cpos_b1cpos,
                               s0cpos_b0cpos_b1cpos]

    if len(state.buff) >= 3:
        # unigram
        b2form = 'b2form' + sentence.form[int(state.buff[2])]
        b2cpos = 'b2cpos' + sentence.cpos[int(state.buff[2])]
        b2formcpos = b2form + b2cpos
        b2feats = 'b2feats' + sentence.feats[int(state.buff[2])]
        # bigram

        # trigram
        b0cpos_b1cpos_b2cpos = b0cpos + b1cpos + b2cpos

        features = features + [b2form, b2cpos, b2formcpos,b2feats,
                               b0cpos_b1cpos_b2cpos]

    if len(state.buff) >= 4:
        # unigram
        b3form = 'b3form' + sentence.form[int(state.buff[3])]
        b3cpos = 'b3cpos' + sentence.cpos[int(state.buff[3])]
        b3formcpos = b3form + b3cpos

        features = features + [b3form,b3cpos,b3formcpos]
    return features

def build_feature_dict(train_sentences):
    feature_dict = {}
    for sentence in train_sentences:
        state = parser.State(sentence)
        gold_arcs = sentence.gold_arcs
        while not parser.is_terminal(state):
            features = feature_extraction(sentence, state)
            for f in features:
                if not feature_dict.get(f):
                    feature_dict[f] = len(feature_dict)
            state, transition = parser.oracle_parsing(state, gold_arcs)

    return feature_dict

def feature_to_index(features, feature_dict):
    feature_id = []
    for f in features:
        try:
            feature_id.append(feature_dict[f])
        except:
            pass
    return feature_id



def get_ld(item, arcs):
    l = [int(child) for head, child in arcs if item == head]
    l.sort()
    if l == []:
        return "None"
    else:
        return str(l[0])

def get_rd(item, arcs):
    l = [int(child) for head, child in arcs if item == head]
    l.sort()
    if l == []:
        return "None"
    else:
        return str(l[-1])

def get_head(item, arcs):
    l = [head for head, child in arcs if item == child]
    if l == []:
        return "None"
    else:
        return l[0]

def get_cpos(item, sentence):
    if item =='None':
        return 'None'
    else:
        return sentence.cpos[int(item)]

def build_pos_dict(train_sentences):
    feature_dict = {}
    for sentence in train_sentences:
        for token in sentence:


    return feature_dict