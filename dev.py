'''

Developing use

'''



import sys
import IO
import eva
import parser
import oracle
import feature
import model
import filecmp
import time

# gold_sentences = IO.Reader('english/train/wsj_train.conll06')
# train_sentences = IO.Reader('english/train/wsj_train.conll06')
# gold_sentences = IO.Reader('english/dev/wsj_dev.conll06.gold')
# train_sentences = IO.Reader('english/dev/wsj_dev.conll06.blind')




# IO Testing

# gold_sentences = IO.Reader('english/train/wsj_train.only-projective.first-1k.conll06')
# print('Testing IO')
# IO.Writer(gold_sentences, 'output')
# if filecmp.cmp('output', 'english/train/wsj_train.only-projective.first-1k.conll06'):
#     print('---> IO is functional!')



# Evaluation Testing

# gold_sentences = IO.Reader('english/dev/wsj_dev.conll06.gold')
# predicted_sentence = IO.Reader('english/dev/wsj_dev.conll06.pred')
# UAS = eva.UAS(gold_sentences, predicted_sentence)
# LAS = eva.LAS(gold_sentences, predicted_sentence)
# print('UAS:', UAS)
# print('LAS:', LAS)



# Oracle Testing

# train_sentences = IO.Reader('english/train/wsj_train.only-projective.conll06')
# fail = 0
# for i in range(len(train_sentences[:100])):
#     state = parser.State(train_sentences[i])
#     gold_arcs = train_sentences[i].gold_arcs
#     while not parser.is_terminal(state):
#         state, transition = parser.oracle_parsing(state, gold_arcs)
#
#     if set(state.arcs) != set(gold_arcs):
#         fail += 1
#         print('Fail in sentence %s' %i)
#     train_sentences[i].head = parser.state2tree(state, train_sentences[i].head)
# if fail>0:
#     print('Fail in %s sentences' %fail)
# else:
#     print('Oracle Sucess!')




# Oracle Testing - one sentence

# train_sentences = IO.Reader('english/train/wsj_train.first-1k.conll06')
# i = 1
# state = parser.State(train_sentences[i])
# gold_arcs = train_sentences[i].gold_arcs
# while not parser.is_terminal(state):
#
#     state, transition = parser.oracle_parsing(state, gold_arcs)
#     print(transition, state.buff, state.stack)




# Output Tree Testing

# gold_sentences = IO.Reader('english/train/wsj_train.only-projective.first-1k.conll06')
# train_sentences = IO.Reader('english/train/wsj_train.only-projective.first-1k.conll06')
# i=0
# state = parser.State(train_sentences[i])
# gold_arcs = gold_sentences[i].gold_arcs
# while not parser.is_terminal(state):
#     state, transition = parser.oracle_parsing(state, gold_arcs)
# train_sentences[i].head = parser.state2tree(state, train_sentences[i].head)
# print(train_sentences[i].head==gold_sentences[i].head)


# gold_sentences = IO.Reader('english/train/wsj_train.only-projective.first-1k.conll06')
# train_sentences = IO.Reader('english/train/wsj_train.only-projective.first-1k.conll06')
# state = parser.State(train_sentences[2])
# print(state.buff, state.stack, state.arcs)
# print(oracle.valid_transition(state))
# while not parser.is_terminal(state):
#     state, transition = parser.oracle_parsing(state, train_sentences[2].gold_arcs)
#     print(state.buff, state.stack, state.arcs)
#     print(oracle.valid_transition(state))


# Test get_dependency

# train_sentences = IO.Reader('english/train/wsj_train.first-1k.conll06')
# i = 2
# state = parser.State(train_sentences[i])
# gold_arcs = train_sentences[i].gold_arcs
# while not parser.is_terminal(state):
#     # print(state.buff[0], state.arcs)
#     print(feature.get_head(state.stack[-1], state.arcs))
#     state, transition = parser.oracle_parsing(state, gold_arcs)



tStart = time.time()

# gold_sentences = IO.Reader('german/dev/tiger-2.2.dev.conll06.gold')
# test_sentences = IO.Reader('german/dev/tiger-2.2.dev.conll06.blind')
# train_sentences = IO.Reader('german/train/tiger-2.2.train.first-5k.conll06')
# train_sentences = IO.Reader('german/train/tiger-2.2.train.conll06')

# gold_sentences = IO.Reader('english/train/wsj_train.first-5k.conll06')
# test_sentences = IO.Reader('english/train/wsj_train.first-5k.conll06')
# train_sentences = IO.Reader('english/train/wsj_train.first-5k.conll06')


gold_sentences = IO.Reader('../english/dev/wsj_dev.conll06.gold')
test_sentences = IO.Reader('../english/dev/wsj_dev.conll06.blind')
train_sentences = IO.Reader('../english/train/wsj_train.first-5k.conll06')
# train_sentences = IO.Reader('english/train/wsj_train.conll06')

# load_model = model.load_model('model_test')
# load_model.random_parsing(test_sentences)

print('Total number of training snetence:', len(train_sentences))
model_basic = model.model(train_sentences, test_sentences, gold_sentences)
iteration = 10
model_basic.train_model(iteration)
# model.save_model(model_basic, 'de')
#
#
tEnd = time.time()
print("It cost %s mins" % ((tEnd - tStart)/60))





# tStart = time.time()
#
# test_sentences = IO.Reader('english/test/wsj_test.conll06.blind')
#
# load_model = model.load_model('model_en')
# load_model.parsing(test_sentences)
# IO.Writer(test_sentences, 'test_en.conll06.pred')
#
#
# test_sentences = IO.Reader('german/test/tiger-2.2.test.conll06.blind')
#
# load_model = model.load_model('model_de')
# load_model.parsing(test_sentences)
# IO.Writer(test_sentences, 'test_de.conll06.pred')
#
# tEnd = time.time()
# print("It cost %f sec" % (tEnd - tStart))