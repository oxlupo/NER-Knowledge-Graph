import requests
from bs4 import BeautifulSoup as bs
import numpy as np
from nltk import word_tokenize
import re
from deeppavlov import configs, build_model
from nltk.corpus import stopwords
from termcolor import colored
ner_model = build_model(configs.ner.ner_ontonotes_bert_torch, download=False)

def connection(url):
    """get text of a website with request library"""
    try:
        data = requests.get(url, verify=False, timeout=10)
    except Exception:
        return Exception
    if data.status_code == 200:

        content = data.content
        soup = bs(content, "html.parser")
        soup = soup.text
        soup = soup.replace("\n", " ")
        return soup
    else:
        return data.status_code

def split_text_by_token(clean_sentences, chunck_size:int):
    """split clean text by 512 if bigger than 512 chunk"""

    text_split_joined = []
    text_tokens = word_tokenize(clean_sentences)
    chunk_size = chunck_size

    our_array = np.array(text_tokens)

    chunked_arrays = np.array_split(our_array, len(text_tokens) // chunk_size + 1)
    chunked_list = [list(array) for array in chunked_arrays]
    for item in chunked_list:
        clean_sentence = (" ").join(item)
        text_split_joined.append(clean_sentence)

    return text_split_joined

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

def tokenize_word_all_sentences(sentences_list):
    text = " ".join(sentences_list)
    text_token = word_tokenize(text)
    token_text_final = [word for word in text_token]
    return [token_text_final]

def collapse(ner_result):
    """
    :param ner_result: our (ner result) looks bad for get relation and we should pair I- with B- pre Prefix
    """
    # List with the result
    collapsed_result = []

    # Buffer for tokens belonging to the most recent entity
    current_entity_tokens = []
    current_entity = None

    # Iterate over the tagged tokens
    for token, tag in ner_result:
        try:
            if tag == "O":
                continue
            # If an enitity span starts ...
            if tag.startswith("B-"):
                # ... if we have a previous entity in the buffer, store it in the result list
                if current_entity is not None:
                    collapsed_result.append(
                        (" ".join(current_entity_tokens), current_entity))

                current_entity = tag[2:]
                # The new entity has so far only one token
                current_entity_tokens = [token]
            # If the entity continues ...
            elif tag == "I-" + current_entity:
                # Just add the token buffer
                current_entity_tokens.append(token)
            else:
                raise ValueError("Invalid tag order.")
        except Exception:
            continue

    # The last entity is still in the buffer, so add it to the result
    # ... but only if there were some entity at all
    if current_entity is not None:
        collapsed_result.append(
            (" ".join(current_entity_tokens), current_entity))
    return collapsed_result

def extract_entity(model):
    """we get entity with deeppavlov """
    entity = model[0][0]
    tag = model[1][0]
    ner = list(map(lambda x, y: (x, y), entity, tag))
    return ner
def in_one_list(list_):
    final_list = []
    for element in list_:
        for el in element:
            final_list.append(el)
    return final_list

def split_by_sentence(sentences):
    """this function for split text by sentences"""
    final_list = []
    if isinstance(sentences, list):
        for sent in sentences:
            try:
                model = ner_model([str(sent)])
                ner = extract_entity(model)
                collapse_ner = collapse(ner)
                final_list.append(collapse_ner)

            except Exception:
                return "TOKEN-SIZE ERROR"

        return final_list
    if isinstance(sentences, str):
        try:
            model = ner_model([str(sentences)])
            ner = extract_entity(model)
            collapse_ner = collapse(ner)
            final_list.append(collapse_ner)
        except RuntimeError:
            raise "an error was appeared in extract NER step"
        except Exception:
            print(Exception)

        return final_list


def extract_product(url):
    chunk_size = 300
    condition = True
    while condition:
        text = connection(url=url)
        if isinstance(text, int):
            print(colored(f"the status code of {url} is >>>> {text} and couldn't got it", 'yellow'))
            condition = False
            pass
        elif str(text) == "<class 'Exception'>":
            print(colored("the domain was invalid", 'yellow'))
            break
        try:
            if not isinstance(text, int):
                clean_text = text_cleaner(text)
                split_by_512_chunk = split_text_by_token(clean_text, chunck_size=chunk_size)
                ner_list = split_by_sentence(sentences=split_by_512_chunk)
                if ner_list == 'TOKEN-SIZE ERROR':
                    chunk_size = chunk_size - 50
                elif not ner_list == 'TOKEN-SIZE ERROR':
                    condition = False
                    ner = in_one_list(ner_list)
                    product = list(filter(lambda x: x if x[1] == "PRODUCT" else False, ner))
                    return product
        except Exception:
            print(Exception)
            
url = "https://www.microsoft.com/en-us"
product = extract_product(url)
print(product)