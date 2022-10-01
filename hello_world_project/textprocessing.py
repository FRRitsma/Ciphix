#%%
from itertools import count
import nltk 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import numpy as np
import os
import pickle

# Constants accessed as globals in function scope:
try:
    ALLOWED_WORDS   = set(nltk.corpus.words.words())
except:
    nltk.download('words')
    ALLOWED_WORDS   = set(nltk.corpus.words.words())

try:
    STOP_WORDS      = set(stopwords.words('english'))
except:
    nltk.download('stopwords')
    STOP_WORDS      = set(stopwords.words('english'))

try:
    _ = word_tokenize("")
except:
    nltk.download("punkt")

def process_sentence(sentence:str, no_repitition:bool = False) -> str:
    """
    Receives senetence as string, returns all relevant English words as a string
    """
    # Type check:
    if type(sentence) is pd.core.series.Series:
        sentence = sentence[0]

    # Tokenize:
    tokenized_sentence = word_tokenize(sentence)

    # Keep only English words:
    tokenized_sentence = [word for word in tokenized_sentence if word in ALLOWED_WORDS]

    # Remove stopwords:
    tokenized_sentence = [word for word in tokenized_sentence if word not in STOP_WORDS]

    # Remove repitition:
    if no_repitition:
        tokenized_sentence = list(set(tokenized_sentence))

    return " ".join(tokenized_sentence)

def prepare_setup() -> None:
    """
    Creates the folder structure used in later stages of development
    """
    root = 'artifacts'
    sub_root = ['', 'data', 'models']
    # Folder for all user created outputs:
    for sub in sub_root:
        path = os.path.join(root, sub)
        if not os.path.isdir(path):
            os.makedirs(path)

def train_lda_model(text_list, n_topics:int = 10, max_features:int = 1000) -> tuple:
    """
    A to Z creation of lda model with associated vocabulary
    """

    # Extract vocabulary/convert to matrix form:
    countvec        = CountVectorizer(max_features=max_features)
    countvec_array  = countvec.fit_transform(text_list).toarray()

    # Fit model:
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=0)
    lda.fit(countvec_array)

    return countvec, lda


class Predictor():
    """
    Integrates several components required for providing a feedback for an input string.
    """
    def __init__(self, countvec, lda) -> None:
        self.countvec = countvec
        self.lda = lda
    def predict(self, input_string:str) -> np.ndarray:
        x = process_sentence(input_string)
        x = self.countvec.transform([x])
        x = self.lda.transform(x)
        return x

#%%

# Only run during development phase:
if __name__ == "__main__":

    # Load all data:
    df_main = pd.read_csv('data.csv', header=None)
    df_main.columns = ['Text']

    # Select subset:
    df_partial = df_main.sample(frac= .01)

    # Tokenize/filter words:
    df_partial["Text"] = df_partial["Text"].apply(process_sentence)

    # Transform to occurences:
    countvec        = CountVectorizer(max_features=1000)
    countvec_array  = countvec.fit_transform(df_partial["Text"]).toarray()
    
    # Train lda model:
    lda = LatentDirichletAllocation(n_components=10, random_state=0)
    lda.fit(countvec_array)

    words = countvec.get_feature_names_out()
    comp1  = lda.components_[5,:]
    topic1 = words[np.argsort(-comp1)]
    print(topic1[0:20])