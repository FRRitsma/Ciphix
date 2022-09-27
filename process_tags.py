# Creating subfunctions for data analysis:
import string

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

def is_user_name(word:str) -> bool:
    """
    Returns true if word is a user name
    """
    if len(word) == 0:
        return False
    return word[0] == '@' and not is_company_name(word)


def has_company_name(sentence:str) -> bool:
    """
    Returns true if string has a company name
    """
    return count_company_names(sentence) > 0

def has_user_name(sentence:str) -> bool:
    for word in sentence.split(' '):
        if word[0] == '@' and not is_company_name(word):
            return True
    return False

def extract_user_names(sentence:str) -> set:
    """
    Extracts all user names
    """
    name_set = {name for name in set(sentence.split(' ')) if is_user_name(name)}
    return name_set

def extract_company_names(sentence:str) -> set:
    """
    Extracts all company names in the form "@company"
    """    
    name_set = {filter_tags(name) for name in set(sentence.split(' ')) if is_company_name(name)}
    return name_set

def count_user_names(sentence:str) -> int:
    """
    Counts the amount of user names in a single tweet
    """
    return len(extract_user_names(sentence))

def count_company_names(sentence:str) -> int:
    """
    Counts the amount of company names in a single tweet
    """
    return len(extract_company_names(sentence))
