import warnings
import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import spacy
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')


def clean_and_tokenize_song(text, model):
    """
    returns a string of cleaned tokens
    
    arguments
    ---------
    text: string
    model: spacy bag-of-words model
    
    return
    ------
    string
    
    """
    
    clean_text = ""
    
    text = text.replace("\n", " ")
    tokens = model(text)
    
    for word in tokens:
        if model.vocab.strings[word.text] in model.vocab:
            if not word.is_stop and not word.is_punct and word.is_alpha:
                clean_text += word.lemma_ + " "
    
    return clean_text


def read_lyricsFiles(songFiles, filepath):
    """
    returns a list containing three lists of
    - artist names, 
    - raw song lyrics and 
    - song titles.
    Only reads files with no square brackets in their names, i.e. no remixes or special versions of the song.
    
    arguments
    ---------
    songFiles: list of strings of song file names
    filepath: directory path to song files 
    
    return
    ------
    string
    
    """
    
    artists = []
    songLyrics = []
    songTitles = []
    for song in songFiles:
        file = open(filepath + song, "r")
        lyrics = file.read()
        artist = song.split("_")[0]
        songTitle = song.split("_")[1]
        if song.split("_")[1].find("[") == -1:
            artists.append(artist)
            songLyrics.append(lyrics)
            songTitles.append(songTitle.replace(".txt",""))
    return [artists, songLyrics, songTitles]

def clean_and_tokenize_lyrics(songLyrics, model):
    """
    returns a list of strings containing tokenized words 
    
    arguments
    ---------
    songLyrics: list of raw song lyrics
    model: spacy bag-of-words model
    
    return
    ------
    string
    
    """
    
    songLyrics_cleaned = []
    for song in songLyrics:
        text_cleaned = clean_and_tokenize_song(song, model)    
        songLyrics_cleaned.append(text_cleaned)
    return songLyrics_cleaned
    
def create_dataframe_lyrics(artists, songLyrics_cleaned, songTitles): 
    """
    returns a dataframe of 
    - artists
    - tokenized words
    - song titles.
    Duplicate rows are dropped.
    
    arguments
    ---------
    artists: list of strings
    songLyrics_cleaned: list of strings containing word tokens
    songTitles: list of strings
    
    
    return
    ------
    dataframe
    
    """
    
    list_of_tuples = list(zip(artists, songLyrics_cleaned, songTitles))   
    df_raw = pd.DataFrame(list_of_tuples, columns = ["artist", "lyrics", "songTitle"])
    df_raw.drop_duplicates(subset = "songTitle", inplace = True)

    return df_raw

def tfdf_bow(cv, tf_corpus):
    """
    returns a dataframe of 
    - artists
    - tokenized words
    - song titles.
    Duplicate rows are dropped.
    
    arguments
    ---------
    artists: list of strings
    songLyrics_cleaned: list of strings containing word tokens
    songTitles: list of strings
    
    
    return
    ------
    dataframe
    
    """
    
    
    #vec_df_bow_cleaned = pd.DataFrame(vec_corpus_bow_cleaned.todense(), columns=cv_bow_cleaned.get_feature_names())
    tf_df_bow = pd.DataFrame(tf_corpus.todense().round(2), columns=cv.get_feature_names())
 
    return tf_df_bow 


def print_model_scores(model, X_train, X_test, y_train, y_test):
    """
    prints scores of a pre-trained scikit-learn model
    
    arguments
    ---------
    model: trained scikit-learn model
    X_train: training data
    X_test: test data
    y_train: target features of the training data
    y_test: target features of the test data
    
    
    return
    ------
    None
    
    """

    print(f'Training Score: {model.score(X_train,y_train)}')
    print(f'Testing Score: {model.score(X_test,y_test)}')



def print_cross_val_results(model, X_train, y_train):
    """
    prints cross-validation scores of a pre-trained model
    
    arguments
    ---------
    model: trained scikit-learn model
    X_train: training data
    X_test: test data
    
    return
    ------
    None
    
    """
        
    accuracy = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    precision = cross_val_score(model, X_train, y_train, cv=5, scoring='precision')
    recall = cross_val_score(model, X_train, y_train, cv=5, scoring='recall')

    print("cross-validation accuracy", accuracy)
    print("\ncross-validation mean", accuracy.mean())
    print("\ncross-validation std", accuracy.std())
    print("\ncross-validation precision", precision)
    print("\ncross-validation mean", precision.mean())
    print("\ncross-validation std", precision.std())
    print("\ncross-validation recall", recall)
    print("\ncross-validation mean", recall.mean())
    print("\ncross-validation std", recall.std())
