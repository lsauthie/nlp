import spacy
from spacy.attrs import LOWER, POS, ENT_TYPE, IS_ALPHA
from spacy.tokens import Doc
import numpy
from collections import deque


class Cosine():
    
    def __init__(self, db):
        
        #https://fasttext.cc/
        #model_bis_path = Path("C:/Users/tk4az/OneDrive/qna/program/model/wiki_news") 
        #self.nlp = spacy.load(model_bis_path)
        #self.nlp = spacy.load('en_core_web_lg') #including vector
        self.nlp = spacy.load('en_core_web_sm') #small only for pos
        
        self.db = db
        self.doc_l = [self.nlp(x[0]) for x in db]
        
    
    def jaccard(self, sen1, sen2):
        
        sen1 = [x.lemma_ for x in sen1 if x.tag_[0] == "N" and not x.is_stop]
        sen2 = [x.lemma_ for x in sen2 if x.tag_[0] == "N" and not x.is_stop]
        
        #jaccard_ratio = len(set(sen1).intersection(sen2)) / float(len(set(sen1).union(sen2)))
        jaccard_ratio = len(set(sen1).intersection(sen2)) / len(set(sen1))
        
        return jaccard_ratio
        
    
    #keep only noun in the sentece - tests were unsuccessfull removing elements from the
    #sentence
    def remove_tokens_on_match(self):
        indexes = []
        for index, token in enumerate(doc):
            if not token.is_stop and token.pos_ == "NOUN":
                indexes.append(index)
        
        np_array = doc.to_array([LOWER, POS, ENT_TYPE, IS_ALPHA])
        np_array = numpy.delete(np_array, indexes, axis = 0)
        doc2 = Doc(doc.vocab, words=[t.text for i, t in enumerate(doc) if i not in indexes])
        doc2.from_array([LOWER, POS, ENT_TYPE, IS_ALPHA], np_array)
        
        return doc2
    
    #comparing two sentences based on the model
    def main(self, sen1, top_x=3):
        
        #[[r,q,a],[r,q,a]]
        output = deque(top_x*[[0,'','']], top_x) #get the top <x> items
        sen1 = self.nlp(sen1)
        
        for inx, x in enumerate(self.doc_l):
            ratio = self.jaccard(sen1, x)

            if ratio > output[0][0]:
                output.appendleft([ratio]+[x.text]+[self.db[inx][1]])

        return list(output)