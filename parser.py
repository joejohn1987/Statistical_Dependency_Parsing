'''
parser.py provides functions to parse a sentence instance
'''


from collections import deque
import oracle

class State:
    def __init__(self, sentence):
        self.buff = deque(sentence.ID[1:])
        self.stack = ['0']
        self.heads = -1
        self.transition = []
        self.arcs = []

def do_shift(state):
    state.stack.append(state.buff[0])
    state.buff.popleft()
    return state

def do_reduce(state):
    state.stack.pop()
    return state

def do_left_arc(state):
    state.arcs.append((state.buff[0], state.stack[-1]))
    state.stack.pop()
    return state

def do_right_arc(state):
    state.arcs.append((state.stack[-1], state.buff[0]))
    state.stack.append(state.buff[0])
    state.buff.popleft()
    return state

def is_terminal(state):
    return not state.buff

def state2tree(state, head_list):
    l = ['_']*len(head_list)
    for head, child in state.arcs:
        l[int(child)] = head
    for i in range(1,len(l)):
        if l[i] == '_' and i == 1:
            l[i] = str(2)
        elif l[i] == '_':
            l[i] = str(i-1)
    return l

def oracle_parsing(state, gold_arcs):
    if oracle.should_left_arc(state, gold_arcs):
        state = do_left_arc(state)
        transition = 0 #'LA'
    elif oracle.should_right_arc(state, gold_arcs):
        state = do_right_arc(state)
        transition = 1 #'RA'
    elif oracle.should_reduce(state, gold_arcs):
        state = do_reduce(state)
        transition = 2 #'RE'
    else:
        state = do_shift(state)
        transition = 3 #'SH'
    return state, transition

def model_parsing(state, transition):
    if transition == 0:
        state = do_left_arc(state)
    elif transition == 1:
        state = do_right_arc(state)
    elif transition == 2:
        state = do_reduce(state)
    elif transition == 3:
        state = do_shift(state)
    return state



