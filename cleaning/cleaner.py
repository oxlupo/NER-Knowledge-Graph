import re
from nltk import word_tokenize
from nltk.corpus import stopwords
import numpy as np

def text_cleaner(text):
    """Because I got the text from Wikipedia,
     the text is not clean for our work, for example,
      it has *[0-9]* and we have to delete it.return clean_sentence, tokens_without_sw """
    pattern = "\[[0-9]+\]"
    text_sub = re.sub(pattern=pattern, repl="", string=text)
    text_tokens = word_tokenize(text_sub)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
    clean_sentence = (" ").join(tokens_without_sw)
    return clean_sentence

def tokenize_word(text):
    """remove stopword from text by using nltk library"""
    text_tokens = word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens]
    return [tokens_without_sw]
def tokenize_word_all_sentences(sentences_list):
    text = " ".join(sentences_list)
    text_token = word_tokenize(text)
    token_text_final = [word for word in text_token]
    return [token_text_final]


def split_text_by_token(clean_sentences):
    """split clean text by 512 if bigger than 512 chunk"""

    text_split_joined = []
    text_tokens = word_tokenize(clean_sentences)
    chunk_size = 300

    our_array = np.array(text_tokens)

    chunked_arrays = np.array_split(our_array, len(text_tokens) // chunk_size + 1)
    chunked_list = [list(array) for array in chunked_arrays]
    for item in chunked_list:
        clean_sentence = (" ").join(item)
        text_split_joined.append(clean_sentence)

    return text_split_joined

