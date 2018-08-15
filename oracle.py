'''
Orcale.py provides different function to check the validity of properties of args and transitions


'''


from collections import deque


def should_left_arc(state, gold_arcs):
    return (state.buff[0], state.stack[-1]) in gold_arcs

def should_right_arc(state, gold_arcs):
    return (state.stack[-1], state.buff[0]) in gold_arcs

def should_reduce(state, gold_arcs):
    return has_head(state.stack[-1], state.arcs) and has_all_children(state.stack[-1], state.arcs, gold_arcs)

def has_head(item, arcs):
    return item in [child for head, child in arcs]

def has_child(item, arcs):
    return item in  [head for head, child in arcs]

def has_all_children(item, state_arcs, gold_arcs):
    if not has_child(item, gold_arcs):
        return True
    children = [child for head, child in gold_arcs if head == item]
    for c in children:
        if (item, c) not in state_arcs:
            return False
    return all([has_all_children(c, state_arcs, gold_arcs) for c in children])

def valid_transition(state):
    transition = []
    if state.stack[-1] != '0' and not has_head(state.stack[-1], state.arcs):
        transition.append(0)
    transition.append(1)
    if state.stack[-1] != '0' and has_head(state.stack[-1], state.arcs):
        transition.append(2)
    transition.append(3)
    return transition