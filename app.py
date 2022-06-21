# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 04:13:44 2022

@author: aniru
"""


#Importing necessary libraries 
from keras.models import load_model
import tensorflow as tf
from flask import Flask, render_template, request
from wtforms import Form, TextField, validators, SubmitField, DecimalField, IntegerField
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nlp 
import snscrape.modules.twitter as sntwitter
import numpy as np 

# Create app
app = Flask(__name__)


class ReusableForm(Form):
    """User entry form for entering specifics for generation"""
    tweetSearch = TextField("Enter the keywords tweet to be got:", validators=[validators.InputRequired()])
    submit = SubmitField("Enter")

class ReusableFormUser(Form):
    tweetSearch = TextField("Enter the username of the user you want to analyse:", validators=[validators.InputRequired()])
    submit = SubmitField("Enter")



#Function calls 
def get_sequences(tokenizer, tweets):
    sequences = tokenizer.texts_to_sequences(tweets)
    
    padded_sequences = pad_sequences(sequences, truncating='post', maxlen=50, padding='post')
    return padded_sequences

def listToString(s):
    str1 = " "  
    return (str1.join(s))

def convertTuple(tup):
        # initialize an empty string
    str = ''
    for item in tup:
        str = str + item
    return str

def convert(list):
    return tuple(i for i in list)

def load_keras_model():
    """Load in the pre-trained model"""
    global model
    path ="C:/Users/aniru/postNonsense/model/twitter_emotion_model.h5"
    model = load_model(path)

#Predefining
classes = {'fear', 'anger', 'surprise', 'love', 'joy', 'sadness'}
classes_to_index = dict((c, i) for i, c in enumerate(classes))
index_to_classes = dict((v, k) for k, v in classes_to_index.items())

#headings= ("Tweet","Emotion")



# Home page
@app.route("/", methods=['GET', 'POST'])
def home():
    """Home page of app with form"""
    # Create form
    form1 = ReusableForm(request.form)
    form2 = ReusableFormUser(request.form)

    # On form entry and all conditions met
    if request.method == 'POST' and form1.validate():
        headings= ("User","Location","Tweet","Emotion")
        tweetSearch = request.form['tweetSearch']
        #print(tweetSearch)
        #records = []
        #records.append(tweetSearch)
        #print(records)
        query = tweetSearch
        limits =10
        tweets =[]
        records= []
        users =[]
        locations = []
        List= []
        pred_emo=" "
        
        for tweet in sntwitter.TwitterSearchScraper(query).get_items():
            if len(tweets) == limits:
                break
            else:
                tweets.append([tweet.date , tweet.user.username, tweet.user.displayname,tweet.content,tweet.user.location,tweet.user.profileImageUrl,tweet.lang,tweet.retweetedTweet ,tweet.inReplyToTweetId,tweet.inReplyToUser,tweet.hashtags])
                records.append([tweet.content])
                users.append([tweet.user.username])
                locations.append([tweet.user.location])
        tokenizer = Tokenizer(num_words=10000, oov_token='<UNK>')
        while limits >0:
            Curr_List = []
            tokenizer.fit_on_texts(records)
            test_sequences = get_sequences(tokenizer, records)
            p = model.predict(np.expand_dims(test_sequences[limits-1], axis=0))[0]
            pred_class=index_to_classes[np.argmax(p).astype('uint8')]
            print(records[limits-1])
            print('Predicted Emotion: ', pred_class)
            #text=' '.join([str(elem) for elem in records[limits-1]])
            #print(type(text))
            #pred_emo+="     \n\n The Predicted Emotion for \n :"+text+" is \n"+pred_class +" \n"
            
            text = records[limits-1]
            user= users[limits-1]
            location =locations[limits-1]
            Curr_List.append(user)
            Curr_List.append(location)
            Curr_List.append(text)
            Curr_List.append(pred_class)
            List.append(tuple(Curr_List))
            limits= limits-1
            
           
        data = tuple(List)    
        #data.append(List)    
        if tweetSearch == 'random':
            #return render_template('random.html', input=generate_random_start(model=model, graph=graph, new_words=words, diversity=diversity))
            return render_template('random.html',prediction_text='CO2 Emission of the vehicle is :{}')
        else:
            #return render_template('seeded.html', input=generate_from_seed(model=model, graph=graph, seed=seed, new_words=words, diversity=diversity))
            return render_template('tables.html', headings = headings , data = data)
    # Send template information to index.html

    # On form entry and all conditions met
    if request.method == 'POST' and form2.validate():
        headings= ("User","Location","Tweet","Emotion")
        tweetSearch = request.form['tweetSearch']
        #print(tweetSearch)
        #records = []
        #records.append(tweetSearch)
        #print(records)
        query = text_part1="(from:"+tweetSearch+")"
        limits =10
        tweets =[]
        records= []
        users =[]
        List= []
        locations = []
        pred_emo=" "
        
        for tweet in sntwitter.TwitterSearchScraper(query).get_items():
            if len(tweets) == limits:
                break
            else:
                tweets.append([tweet.date , tweet.user.username, tweet.user.displayname,tweet.content,tweet.user.location,tweet.user.profileImageUrl,tweet.lang,tweet.retweetedTweet ,tweet.inReplyToTweetId,tweet.inReplyToUser,tweet.hashtags])
                records.append([tweet.content])
                users.append([tweet.user.username])
        tokenizer = Tokenizer(num_words=10000, oov_token='<UNK>')
        while limits >0:
            Curr_List = []
            tokenizer.fit_on_texts(records)
            test_sequences = get_sequences(tokenizer, records)
            p = model.predict(np.expand_dims(test_sequences[limits-1], axis=0))[0]
            pred_class=index_to_classes[np.argmax(p).astype('uint8')]
            print(records[limits-1])
            print('Predicted Emotion: ', pred_class)
            #text=' '.join([str(elem) for elem in records[limits-1]])
            #print(type(text))
            #pred_emo+="     \n\n The Predicted Emotion for \n :"+text+" is \n"+pred_class +" \n"
            
            text = records[limits-1]
            user= users[limits-1]
            location =locations[limits-1]
            Curr_List.append(user)
            Curr_List.append(location)
            Curr_List.append(text)
            Curr_List.append(pred_class)
            List.append(tuple(Curr_List))
            limits= limits-1
            
           
        data = tuple(List)    
        #data.append(List)    
        if tweetSearch == 'random':
            #return render_template('random.html', input=generate_random_start(model=model, graph=graph, new_words=words, diversity=diversity))
            return render_template('random.html',prediction_text='CO2 Emission of the vehicle is :{}')
        else:
            #return render_template('seeded.html', input=generate_from_seed(model=model, graph=graph, seed=seed, new_words=words, diversity=diversity))
            return render_template('tables.html', headings = headings , data = data)
    # Send template information to index.html
    return render_template('index.html', form1=form1 , form2= form2)


@app.route("/index.html", methods=['GET', 'POST'])
def index():
    """Home page of app with form"""
    # Create form
    form1 = ReusableForm(request.form)
    form2 = ReusableFormUser(request.form)

    # On form entry and all conditions met
    if request.method == 'POST' and form1.validate():
        headings= ("User","Location","Tweet","Emotion")
        tweetSearch = request.form['tweetSearch']
        #print(tweetSearch)
        #records = []
        #records.append(tweetSearch)
        #print(records)
        query = tweetSearch
        limits =10
        tweets =[]
        records= []
        users =[]
        locations = []
        List= []
        pred_emo=" "
        
        for tweet in sntwitter.TwitterSearchScraper(query).get_items():
            if len(tweets) == limits:
                break
            else:
                tweets.append([tweet.date , tweet.user.username, tweet.user.displayname,tweet.content,tweet.user.location,tweet.user.profileImageUrl,tweet.lang,tweet.retweetedTweet ,tweet.inReplyToTweetId,tweet.inReplyToUser,tweet.hashtags])
                records.append([tweet.content])
                users.append([tweet.user.username])
                locations.append([tweet.user.location])
        tokenizer = Tokenizer(num_words=10000, oov_token='<UNK>')
        while limits >0:
            Curr_List = []
            tokenizer.fit_on_texts(records)
            test_sequences = get_sequences(tokenizer, records)
            p = model.predict(np.expand_dims(test_sequences[limits-1], axis=0))[0]
            pred_class=index_to_classes[np.argmax(p).astype('uint8')]
            print(records[limits-1])
            print('Predicted Emotion: ', pred_class)
            #text=' '.join([str(elem) for elem in records[limits-1]])
            #print(type(text))
            #pred_emo+="     \n\n The Predicted Emotion for \n :"+text+" is \n"+pred_class +" \n"
            
            text = records[limits-1]
            user= users[limits-1]
            location =locations[limits-1]
            Curr_List.append(user)
            Curr_List.append(location)
            Curr_List.append(text)
            Curr_List.append(pred_class)
            List.append(tuple(Curr_List))
            limits= limits-1
            
           
        data = tuple(List)    
        #data.append(List)    
        if tweetSearch == 'random':
            #return render_template('random.html', input=generate_random_start(model=model, graph=graph, new_words=words, diversity=diversity))
            return render_template('random.html',prediction_text='CO2 Emission of the vehicle is :{}')
        else:
            #return render_template('seeded.html', input=generate_from_seed(model=model, graph=graph, seed=seed, new_words=words, diversity=diversity))
            return render_template('tables.html', headings = headings , data = data)
    # Send template information to index.html

    # On form entry and all conditions met
    if request.method == 'POST' and form2.validate():
        headings= ("User","Location","Tweet","Emotion")
        tweetSearch = request.form['tweetSearch']
        #print(tweetSearch)
        #records = []
        #records.append(tweetSearch)
        #print(records)
        query = text_part1="(from:"+tweetSearch+")"
        limits =10
        tweets =[]
        records= []
        users =[]
        List= []
        locations = []
        pred_emo=" "
        
        for tweet in sntwitter.TwitterSearchScraper(query).get_items():
            if len(tweets) == limits:
                break
            else:
                tweets.append([tweet.date , tweet.user.username, tweet.user.displayname,tweet.content,tweet.user.location,tweet.user.profileImageUrl,tweet.lang,tweet.retweetedTweet ,tweet.inReplyToTweetId,tweet.inReplyToUser,tweet.hashtags])
                records.append([tweet.content])
                users.append([tweet.user.username])
        tokenizer = Tokenizer(num_words=10000, oov_token='<UNK>')
        while limits >0:
            Curr_List = []
            tokenizer.fit_on_texts(records)
            test_sequences = get_sequences(tokenizer, records)
            p = model.predict(np.expand_dims(test_sequences[limits-1], axis=0))[0]
            pred_class=index_to_classes[np.argmax(p).astype('uint8')]
            print(records[limits-1])
            print('Predicted Emotion: ', pred_class)
            #text=' '.join([str(elem) for elem in records[limits-1]])
            #print(type(text))
            #pred_emo+="     \n\n The Predicted Emotion for \n :"+text+" is \n"+pred_class +" \n"
            
            text = records[limits-1]
            user= users[limits-1]
            location =locations[limits-1]
            Curr_List.append(user)
            Curr_List.append(location)
            Curr_List.append(text)
            Curr_List.append(pred_class)
            List.append(tuple(Curr_List))
            limits= limits-1
            
           
        data = tuple(List)    
        #data.append(List)    
        if tweetSearch == 'random':
            #return render_template('random.html', input=generate_random_start(model=model, graph=graph, new_words=words, diversity=diversity))
            return render_template('random.html',prediction_text='CO2 Emission of the vehicle is :{}')
        else:
            #return render_template('seeded.html', input=generate_from_seed(model=model, graph=graph, seed=seed, new_words=words, diversity=diversity))
            return render_template('tables.html', headings = headings , data = data)
    # Send template information to index.html
    return render_template('index.html', form1=form1 , form2= form2)

if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    load_keras_model()
    # Run app
    app.run(host="0.0.0.0", port=80)