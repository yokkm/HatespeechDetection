### OUTPUT DESCRIPTION 
main.py /predictive

#### AlertLevel scoring 0-4
    0   :   a very clean text no sense of harm nor hatespeech/ words were detected
        Admin attention: no/ a small attention from admin is required
        example: i will survive, where is the nearest bookstore, i love you baby, how to call this thing?
        
    1   :   the comment may contains some bad/toxic words or show a little sign of negativity, however overall sense of comment remain positive. part of word maybe censored if its contains toxic/profanity/ offensive/ 
        Admin attention: a small attention/ regular schedule to check is required
        example: i love you a******(asshole), woahh this is awesome as f***!(fuck)
        
    2   :   the comment contains a lot of bad words/ hatespeech and there is a sign high toxicity for overall comment, first reaction from system will return (WHOLE COMMENT IS HIDED), user who post the comment will still be able to see but hided to public unless admin decide otherwise.
        Admin attention: require moderate attention as the system will hided comment first, then decide to leave it where it is or let or allow the comment to pass
        example: suck my dick, fucking hell, 3klans stupid cunt!
        
    3   :   the comment contains rude words, thos toxic word will be censored and the comment will allow to show to the public
        Admin attention: small attention required, as the sentence will be censored bad words
        example: f*** h***, ca'nt find any good place to dine around here(fucking hell), how's your summer going bitches, I was f*** up last night too much party i guess, you should die, this is so g**(gay), you are racist
        
    4   :   the comment contains sense of threat either suicidal, terrorist, the whole comment will show to public unless it contains bad words(those will be censored)
        Admin attention: IMMEDIATELY attention is required, as this comment tend to show sign of threat to one's life. Admin might need to contact the user who post or related agency that could help to this matter.
        example: there is a bomb, i will cut myself and let it bleed, I will bring a gun to school tomorrow, was prepared to die, m********(motherfuckerrrrrrrr)
        
        
#### HatespeechTag scoring 1-4

    1   :   No hatespeech, offensive, profanity, obscene words detected within the comment
        example: you should die, love you, go away i hate you, dont wanna see you anymore
        
    2   :   swear words, sarcasm words were detected
        example: fuck this unit, i'll try next time., motherfuckerrrr, asshole you should die
        
    3   :   obscence words/ dirty words were detected
        example: suck my dick, i'm naked wanna see?
        
    4   :   Racial, gender, ethnic slurs were detected
        example: klan is stupid, what's up nigga, wanna go back to the time when nazi is glory, black people should stayed as a slave
        

#### CommentTag

    *     Statement   : regular sentence, showing suggestion eg.I'm good thanks
    *   ynQuestion  : starts with verb to be asking for yes/no answer eg. are you kidding me?
    *   whQuestion  : starts with wh-, how eg. how are you
    *   Clarify     : statements tend to ask for opinion eg. black or white
    *   nAnswer     : show sense of answer to one's question eg. i'm a new student here
    *   Greet       : greeting sentence eg.hi there 
        
#### FinalOutput     : comments that already processed and cleaned, can  be serve as an output

#### OriginalText    : original post from user

#### HatespeechType  
    
    *   None        : n/a
    
    *   obscene     : dirty words, profanity
    
    *   sacrcasm    : swear words, tend to use regulary
    
    *   threat      : words that tend to harm one's life
    
    *   racial slurs: words that tends to offense one's nationality
    
    *   ethnic slurs: words that tends to offense one's ethnicity
    
    *   gender slurs: gender bias/ or words that offense one's gender



### Dependcy files
    * big.txt
    
    * .pkl
    
        *  correct_repeatedBadWords.pkl 
        *  read_abbre.pkl
        * Newall_called.pkl :: located in Gdrive
    * .py
    
        * read_ abbre_main.py
        * sonar_func.py





Another dependency (750mb) need to be collected:: located in Gdrive

