#!/usr/bin/env python
# coding: utf-8

# In[9]:


#1
import os
os.environ['KERAS_BACKEND'] = 'tensorflow'
from theano import *
import keras 
import flask
from flask import Flask, request, jsonify, render_template
import json



import warnings
warnings.filterwarnings('ignore')

import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob, Word, Blobber
import tensorflow as tf
from tensorflow.python.keras.backend import set_session
sid = SentimentIntensityAnalyzer()

# Explore vocabulary
import collections
from tqdm import tqdm

from profanity_check import predict, predict_prob
from nltk.tokenize import sent_tokenize, word_tokenize

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from pyspark.sql.types import *

from read_abbre_main import *
from sonar_func import *


# In[15]:


#3

    
with open('correct_repeatedBadWords.pkl', 'rb') as f:
#with open('/Users/yokk/HS/2correct_repeatedBadWords.pkl', 'rb') as f:

    correct_repeatedBadWords=dill.load(f)
    badwords_lst=dill.load(f)
    typeof_bad = dill.load(f)
    badwords = dill.load(f)##
    

import warnings
warnings.filterwarnings('ignore')


# In[16]:


def chkchk(word):
    new_words_list=[]
    for index,item in enumerate(word.split()):
        for e in badwords['word']:
            if e == item:
                new_words_list.append(e)
    return new_words_list

def censor(word):
    new_words_list=''
    for i,item in enumerate(word.split()):
        if predict_prob([item])>=0.3 or item in chkchk(word):#(e for e in badwords['word'] if e == item ):#any(badword in item for badword in badwords_lst):
            item = item[0]+'*'*len(item[1:])
        new_words_list += item+" "
        
    return new_words_list

def comment_type(string):
    s=[]
    com_type=[]
    for i in string.split():
        ss = sid.polarity_scores(i)
        top = ss['compound']
        s.append([top,i])
        com_type.append(i)
    a=min(s)
    min_word = a[1]
    min_word_score = a[0]

    for k in typeof_bad:
        for val in typeof_bad[k]:
            if min_word == val:
                return k
            
    for i in com_type:
        for k in typeof_bad:
            for val in typeof_bad[k]:
                if i == val:
                    return k
    return 'None'


# In[18]:


#7
with open('New_allcalled.pkl', 'rb') as c:
    model = dill.load(c)
    classifier = dill.load(c)
    predictions = dill.load(c)
    dialogue_act_features = dill.load(c)
    max_len = dill.load(c)
    tokenizer = dill.load(c)

app = Flask(__name__)

@app.route('/')
def x():
    return ("--test @app.route--")


@app.route('/predictive',methods=["POST"])
def toxicity_level():
	### For testing json### please refer to test_sample.json

    if request.method =='POST':

        text = request.json
        #text = [val for key, val in text.items() if key =='comment_text']
        text = text['comment_text']
        
        

        
        typeflag=''
        #line = text
        removerepeatword=abbre_then_replace(text)#correct_repeatedBadWords(text)
        ans=classifier.classify(dialogue_act_features(removerepeatword))
        ss = sid.polarity_scores(removerepeatword)
        sonar_topclass,sonar_hate_score,sonar_offen_score,sonar_none_score = sonar_check(removerepeatword)




        new_words_list = []
        type_tag=[]





        # Process string
        new_string = [removerepeatword]
        new_string = tokenizer.texts_to_sequences(new_string)
        new_string = pad_sequences(new_string, maxlen=max_len, padding='post', truncating='post')


        # Predict
        prediction = model.predict(new_string).tolist()
        #find comment type
        comm_type =comment_type(removerepeatword)

        if comm_type =='obscence':
            typeflag=3
        elif comm_type =='threat' or comm_type =='racial slur'or comm_type=='gender slur' or comm_type =='ethnic slur':
            typeflag=4
        elif comm_type =='None':
            typeflag=1
        elif comm_type =='swear words' or comm_type =='sarcasm':
            typeflag=2
        else:typeflag=1
            

	#[0][0] toxicity
        if sonar_topclass =='neither':
            if ss['compound'] <0:
            #'''tentative to be really harm or a threat need immediately attention'''
            #i will cut myself, and let it bleed
                flag = 4
                new_words_list = censor(removerepeatword)
            elif ss['compound'] <0 and typeflag == 1:
                flag = 4
                new_words_list = censor(removerepeatword)
            else:
                flag=0
                new_words_list = censor(removerepeatword)

        else:
            if sonar_topclass !='neither':
                if ss['pos'] >=0.4 and sonar_none_score >=0:
                    new_words_list = removerepeatword
                    flag = 1
                elif ss['compound'] <=0.05 and ss['neg']>= 0.75:
               # '''comment tend to contain extremely rude/ 
                #offensive comment then will hide but will sent alert as 2'''
                    if typeflag!= 1 and typeflag!=2 and typeflag!=3:
                        new_words_list = censor(removerepeatword)
                        flag =3
                    else:
                        cc='Whole comment is hide'
                        new_words_list.append(cc)
                        flag=2
                elif ss['compound'] <=0.05 and ss['neg']< 0.75:
                    new_words_list = censor(removerepeatword)
                #let's go to the beach bitches
                    flag=3
                else:
                    new_words_list = censor(removerepeatword)
                #i love you asshole
                    flag=1
            else:
                pass

        



        joinwords = "".join(new_words_list)
        printdict = {"OriginalText":text,"FinalOutput":joinwords, "HatespeechType":comm_type
                     , "CommentTag":ans,"AlertLevel": flag, "HatespeechTag":typeflag}
        '''
                    ,"ss['compound']":ss['compound'],"ss['neg']":ss['neg'],"ss['pos']":ss['pos']
                    ,"sonar_topclass":sonar_topclass,"sonar_hate_score":sonar_hate_score
                     ,"sonar_offen_score":sonar_offen_score,"sonar_none_score":sonar_none_score}
                         '''
        

#        return printdict#jsonify(printdict)
        return jsonify(printdict)
    else:
        return None
    
if __name__=="__main__":
    #app.run(debug=False, host='0.0.0.0', port=8080)
    app.run(threaded=False,debug=False, host='0.0.0.0',port=80)


# In[5]:

#last update 10/1/2020
#toxicity_level("1 h8 night nig nude fuckkk shittt school mass fuckkkkkkkkkk shooting mast3rb8 suicide retards kill myself m0th3rfuck3r 2MORO")


# In[ ]:



