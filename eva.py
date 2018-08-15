'''
eva provides two method (UAS and LAS) to evaluate the prediction
UAS = correct head/no. of token
LAS = correct head with correcct label/no. of token
'''


def UAS(Gold, Pred):
    correct_head = 0
    total_token = 0
    for i in range(len(Gold)):
        for j in range(1,len(Gold[i].ID)):
            if Gold[i].head[j] == Pred[i].head[j]:
                correct_head += 1
            total_token += 1
        
    score = correct_head / total_token
    return score

def LAS(Gold, Pred):
    correct_label_head = 0
    total_token = 0
    for i in range(len(Gold)):
        for j in range(1,len(Gold[i].ID)):
            if Gold[i].derpel[j] == Pred[i].derpel[j] and Gold[i].head[j] == Pred[i].head[j]:
                correct_label_head += 1
            total_token += 1

    score = correct_label_head / total_token
    return score
