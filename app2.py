# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 01:27:06 2022

@author: aniru
"""


# Neccesary Library Functions to be imported before use 
from flask import Flask, render_template, request
from wtforms import Form, TextField, validators, SubmitField, DecimalField, IntegerField
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import CountVectorizer
import nlp 
import snscrape.modules.twitter as sntwitter
import numpy as np 
import pickle
from nltk.util import pr
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import string
import joblib

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



def listToString(s):

    str1 = ""
    for ele in s:
        str1 += ele
    return str1

def convertTuple(tup):
        # initialize an empty string
    str = ''
    for item in tup:
        str = str + item
    return str

def convert(list):
    return tuple(i for i in list)

# Function to load the model
def load_tree_model():
    global model_tree
    global vectorizer
    # Loading neccesary 
    vectorizer_path = "C:/Users/aniru/datasets/Hate Speech Detection/Davidson_Dataset/vectorizer.pkl"
    vectorizer = joblib.load(vectorizer_path)
    path ="C:/Users/aniru/datasets/Hate Speech Detection/Davidson_Dataset/model/model_decision_Tree.pkl"
    model_tree = pickle.load(open(path, 'rb'))

def generateClassification(msg_list):
    vector = vectorizer.transform(msg_list).toarray()
    classification = model_tree.predict(vector)
    classification = listToString(classification)
    return classification    

def dealFormData():
    headings= ("User","Location","Tweet","Emotion")
    tweetSearch = request.form['tweetSearch']
    query = tweetSearch
    limits =10
    tweets =[]
    records= []
    users =[]
    locations = []
    List= []
    pred_emo=" "
    count  = 0 
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if len(tweets) == limits:
            break
        else:
            if tweet.lang != 'en':
                limits+=1
                continue
            elif len(tweet.content)<30:
                limits+=1
                continue
            tweets.append([tweet.date , tweet.user.username, tweet.user.displayname,tweet.content,tweet.user.location,tweet.user.profileImageUrl,tweet.lang,tweet.retweetedTweet ,tweet.inReplyToTweetId,tweet.inReplyToUser,tweet.hashtags])
            records.append(tweet.content)
            users.append(tweet.user.username)
            locations.append(tweet.user.location)
            count+=1
    while count >0:
        Curr_List = []
        pred_class = generateClassification([records[count-1]])
        print(records[count-1])
        print('Predicted Emotion: ', pred_class)
        text = records[count-1]
        user= users[count-1]
        location =locations[count-1]
        Curr_List.append(user)
        Curr_List.append(location)
        Curr_List.append(text)
        Curr_List.append(pred_class)
        List.append(tuple(Curr_List))
        count= count-1
    return List
    
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
        list_values = dealFormData()
        data = tuple(list_values)
        return render_template('tables.html', headings = headings , data = data)

    # On form entry and all conditions met
    if request.method == 'POST' and form2.validate():
        headings= ("User","Location","Tweet","Emotion")
        list_values = dealFormData()
        data = tuple(list_values)
        return render_template('tables.html', headings = headings , data = data)
       
    # Send template information to index.html
    return render_template('index.html', form1=form1 , form2= form2)



if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    load_tree_model()
    # Run app
    app.run(host="0.0.0.0", port=80)