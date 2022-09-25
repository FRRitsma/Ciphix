#%%
import ipykernel
import string
from bdb import Breakpoint
import pandas as pd
import numpy as np
import tabulate
import colorama
from colorama import Fore
import json
import os

df_main = pd.read_csv('data.csv', header=None)
df_main.columns = ['Text']

#%%
def filter_tags(tag:str) -> str:
    """
    Removes punctuation from a company name tag. Returns string unaltered if not a company name
    """
    if is_company_name(tag):
        tag = '@' + tag.translate(str.maketrans('', '', string.punctuation))
    return tag

def is_company_name(word:str) -> bool:
    """
    Function returns true if a word is the name of a company
    """
    # Word must have minimal length:
    if len(word) < 2:
        return False
    # Must start with "@"-symbol:
    if word[0] != '@':
        return False
    # Second letter must be non-numeric:
    if not word[1].isnumeric():
        return True
    return False

def extract_company_names(sentence:str) -> set:
    """
    Extracts all company names in the form "@company"
    """    
    name_set = {filter_tags(name) for name in set(sentence.split(' ')) if is_company_name(name)}
    return name_set

def count_company_names(sentence:str) -> int:
    """
    Counts the amount of company names in a single tweet
    """
    return len(extract_company_names(sentence))

#%% Split the dataframe into separate conversations

# Can multiple users be addressed in the same tweet?

# Can multiple companies be addresssed in the same tweet?
int_company_names = 0
# How many people can be addressed in the same tweet?
adressed_companies = set()

# for j,i in enumerate(df_main.iterrows()):
#     sentence = i[1][0]
#     if count_company_names(sentence) > int_company_names:
#         print(extract_company_names(sentence))
#     int_company_names = max(int_company_names, count_company_names(sentence))

#     if count_company_names(sentence) > 0:
#         if len(extract_company_names(sentence).intersection(adressed_companies)) == 0:
#             adressed_companies = extract_company_names(sentence)
#             print(sentence)

#%%
# Step 1: Recognize if a tweet is a help request

# Create a data set of help request/not a help request
if os.path.isfile('helprequest.json'):
    with open('helprequest.json', 'r') as fs:
        data = json.load(fs)
    pass
else:
    data = {}
pd.set_option('display.max_colwidth', None)


def labeling_text(df:pd.core.frame.DataFrame, data:dict) -> None:
    
    # Choose random tweet:
    idx = np.random.randint(len(df))
    idx = np.clip(idx,2,len(df)-2)
    
    # Display context and insturctions:
    print(Fore.GREEN + df_main.iloc[idx-2][0])
    print(Fore.GREEN + df_main.iloc[idx-1][0])
    print(Fore.RED + df_main.iloc[idx][0])
    print(Fore.GREEN + df_main.iloc[idx+1][0])
    print(Fore.GREEN + df_main.iloc[idx+2][0])
    print(Fore.WHITE + """ 'a' if NOT a question, 'd' for a question, 'q' to exit """ )

    # Receive input:
    _input = input()

    # Save results:
    with open('helprequest.json', 'w') as fs:
        json.dump(data, fs)

    # Exit button:
    if _input == 'q':
        return
    # Not a question:
    if _input == 'a':
        data[df_main.iloc[idx][0]] = 0
    # Question:
    if _input == 'd':
        data[df_main.iloc[idx][0]] = 1
    # New round of questions:
    labeling_text(df, data)

labeling_text(df_main, data)

#%% Analyze tweets addressed to companies

# 0: Non-Sequiturs

# 1: Initialization

# 2: Continuation

# 3: Conclusion