#%% Import modules:
import json
import os
import numpy as np
import pandas as pd
import colorama
from colorama import Fore

# User defined function:
def labeling_text(data_frame:pd.core.frame.DataFrame, data:dict) -> None:
    """
    Function that allows for quick labeling of data via cli input
    """
    # Choose random tweet:
    idx = np.random.randint(len(data_frame))
    idx = np.clip(idx,2,len(data_frame)-2)
    
    # Display context and insturctions:
    print(Fore.GREEN + data_frame.iloc[idx-2][0])
    print(Fore.GREEN + data_frame.iloc[idx-1][0])
    print(Fore.RED + data_frame.iloc[idx][0])
    print(Fore.GREEN + data_frame.iloc[idx+1][0])
    print(Fore.GREEN + data_frame.iloc[idx+2][0])
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
        data[data_frame.iloc[idx][0]] = 0
    # Question:
    if _input == 'd':
        data[data_frame.iloc[idx][0]] = 1
    # New round of questions:
    labeling_text(data_frame, data)


#%% Load data:
df_main = pd.read_csv('data.csv', header=None)
df_main.columns = ['Text']

if os.path.isfile('helprequest.json'):
    with open('helprequest.json', 'r') as fs:
        data = json.load(fs)
    pass
else:
    data = {}

#labeling_text(df_main, data)
