#!/usr/bin/env python
# coding: utf-8

# In[1]:
import pandas as pd
import dill
import re
import pandas as pd
from collections import Counter
from profanity_check import predict, predict_prob
import os
import warnings
warnings.filterwarnings('ignore')


# In[2]:
cwd = os.getcwd()
read_abbre_path = os.path.join(cwd, "read_abbre.pkl")

'''Load dilled .pkl so that we dont have to worry about the funciton'''
with open(read_abbre_path, 'rb') as f:
    abbre_df=dill.load(f)
    abbre_dict=dill.load(f)
    read_abbre=dill.load(f)

# In[3]:


def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


# In[4]:


# to->from of digits to string
replacements = {'1': 'i', '2': 's', '3': 'e', '4': 'a', '5': 's','0':'o'
                ,'8':'ate','@':'a','$':'s','_':"",'-':"",".":""}

def replace_digit_string(word):
    replace_dig_str=""
    for i in word.split():
        for k,v in replacements.items():
            i = i.replace(k,v)  
        replace_dig_str = replace_dig_str+" "+i
    return correct_string(replace_dig_str)


# In[5]:


def abbre_then_replace(word):
    ans=read_abbre(word)
    return replace_digit_string(ans)


# In[13]:


def correct_string(word):
    correct_str=''
    for i in word.split():
        correct_str = correct_str+" "+correction(i)
    return modify(correct_str)


# In[14]:


#abbre_then_replace('i h8 yuo fuckin c-u-n-t, yuo shold  dickh3adddddd fuckkkkkkk di3 @$$h0l3 - i will k1ll u @TEOTD')


# In[12]:


def modify(word):
    new_words_list=[]
    out=''
    for i in word.split():
        if len(i)>5:
            out = re.sub(r'([a-z])\1+$', r'\1', i)
            out = re.sub(r'^([a-z])\1+', r'\1', out)
            new_words_list.append(out)
        else:
            new_words_list.append(i)
    new_words_list=' '.join(new_words_list)
        
    return new_words_list
#modify(abbre_then_replace('i h8 yuo fuckin c-u-n-t, yuo shold  dickh3adddddd fuckkkkkkk di3 @$$h0l3 - i will k1ll u @TEOTD'))


# In[ ]:




