#!/usr/bin/env python
# coding: utf-8

# In[1]:


from hatesonar import Sonar
sonar = Sonar()
def sonar_check(string):
    sonar_lang = string
    sonar_lang=sonar.ping(string)
    sonar_topclass = sonar_lang['top_class']
    sonar_hate=sonar_lang['classes'][0]
    sonar_offen=sonar_lang['classes'][1]
    sonar_none=sonar_lang['classes'][2]
    
    sonar_hate_score =float(sonar_hate['confidence'])
    sonar_offen_score=float(sonar_offen['confidence'])
    sonar_none_score=float(sonar_none['confidence'])
    return sonar_topclass,sonar_hate_score,sonar_offen_score,sonar_none_score


# In[ ]:



