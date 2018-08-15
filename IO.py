'''
IO.py provides input/ouput method to read or write conll files.
The data is saved as Sentence instances.

'''


class Sentence:
    def __init__(self, sentence_data):
        # Add Root
        self.ID = ['0']
        self.form = ['ROOT']
        self.lemma = ['ROOT']
        self.cpos = ['ROOT']
        self.pos = ['_']
        self.feats = ['_']
        self.head = ['_']
        self.derpel = ['ROOT']
        self.phead = ['_']
        self.pderpel = ['_']
        self.gold_arcs = []

        for token in sentence_data:
            self.fields = token.split('\t')
            self.ID.append(self.fields[0])
            self.form.append(self.fields[1])
            self.lemma.append(self.fields[2])
            self.cpos.append(self.fields[3])
            self.pos.append(self.fields[4])
            self.feats.append(self.fields[5])
            self.head.append(self.fields[6])
            self.derpel.append(self.fields[7])
            self.phead.append(self.fields[8])
            self.pderpel.append(self.fields[9])
            if (self.fields[6]!= '_'):
                self.gold_arcs.append((self.fields[6], self.fields[0]))

def Reader(path):
    # Read lines and build Sentence instances
    with open(path, 'r') as f:
        data = f.readlines()
    sentences = []
    current_sentence_data = []
    for line in data:
        if line != '\n':
            current_sentence_data.append(line)        
        else:
            sentences.append(Sentence(current_sentence_data))
            current_sentence_data = []
    return sentences
            
def Writer(sentences, path):
    with open(path, 'w') as f:
        for sentence in sentences:
            # Remove Root
            for i in range(1,len(sentence.ID)):
                f.write(sentence.ID[i]+'\t'+
                        sentence.form[i]+'\t'+
                        sentence.lemma[i]+'\t'+
                        sentence.cpos[i]+'\t'+
                        sentence.pos[i]+'\t'+
                        sentence.feats[i]+'\t'+
                        sentence.head[i]+'\t'+
                        sentence.derpel[i]+'\t'+
                        sentence.phead[i]+'\t'+
                        sentence.pderpel[i])
            f.write('\n')
