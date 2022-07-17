import termcolor
from deeppavlov.core.commands.utils import parse_config
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
from spacy.matcher import Matcher
from deeppavlov import configs, build_model
nlp = spacy.load('en_core_web_sm')
nltk.download('stopwords')

############---------***READ THE TEXT FROM FOLDER:ABOUT US ***---------############
file = open('apple.txt', 'r', encoding='utf-8')
text = file.read()
############------------***  CLEANING STEP  ***-----------------##################

def text_cleaner(text):
    """Because I got the text from Wikipedia,
     the text is not clean for our work, for example,
      it has *[0-9]* and we have to delete it.return clean_sentence, tokens_without_sw """
    pattern = "\[[0-9]+\]"
    text_sub = re.sub(pattern=pattern, repl="", string=text)
    text_tokens = word_tokenize(text_sub)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
    clean_sentence = (" ").join(tokens_without_sw)
    return [clean_sentence, tokens_without_sw]

ner_list = [('Apple Inc.', 'ORG'), ('American', 'NORP'), ('Apple', 'ORG'), ('Apple', 'ORG'), ('Apple Park', 'FAC'), ('Cupertino', 'GPE'), ('California', 'GPE'), ('Apple', 'ORG'), ('1976', 'DATE'), ('Steve Wozniak', 'PERSON'), ('Steve Jobs', 'PERSON'), ('Ron Wayne', 'PERSON'), ('first', 'ORDINAL'), ('Apple', 'ORG'), ('Lisa', 'PRODUCT'), ('Macintosh', 'PRODUCT'), ('iPod', 'PRODUCT'), ('2001', 'DATE'), ('iPhone', 'PRODUCT'), ('2007', 'DATE'), ('iPad', 'PRODUCT'), ('2010', 'DATE'), ('Apple', 'ORG'), ('day', 'DATE'), ('recent years', 'DATE'), ('iPhone', 'PRODUCT'), ('Apple', 'ORG'), ('50 %', 'PERCENT'), ('iTunes', 'ORG'), ('2003', 'DATE'), ('first', 'ORDINAL'), ('Today', 'DATE'), ('iTunes Store App Store', 'ORG'), ('2008', 'DATE'), ('two', 'CARDINAL')]

############------------***  INTERVALVING STEP  ***-----------------##################
def text_interrupted(text):

    """This function display words in text in intervals type
     like [apple, [0, 1]]
     to make it easier to find relation between NER and verb"""
    clean_data = text_cleaner(text=text)
    list_ = []
    interval_word = []
    for index, token in enumerate(clean_data[1]):

        interval = [token, [index, index + 1]]
        interval_word.append(interval)
    return interval_word
text_interrupted(text=text)

def ner_interrupted(ner_list, interval_word):
    """
    :param ner_list:[('Apple Inc.', 'ORG'), ('American', 'NORP')] Give the function values in this way you can get with deeppavlov Library
    :param interval_word: you get this with text_interrupted function
    :return: and return only interval of NER like this ----> [['Apple', [0, 1]], ['Inc.', [1, 2]], ['Apple', [25, 26]]]
    """
    ner = list(map(lambda x: x[0], ner_list))
    check = []
    for index, token in enumerate(ner):

        token_list = token.split(" ")
        number_of_token = len(token_list)
        first_interval = []
        for interval in (interval_word):

            for entity in token_list:
                if entity == interval[0]:
                    first_interval.append(interval)
        check.append(first_interval)
    check_ = []
    for pair in check:
        if not pair in check_:
            check_.append(pair)
    return check_



def pair_ner_with_text(ner_interval):
    """
    at final function for get interval for our NER we should
    pair the ner interval with text interval for found relation
    :return like this ---> [[' Apple Inc.', [0, 2]], [['American', [2, 3]]], [' Apple Park', [39, 41]]
    """
    final_list = []
    ind = 0
    for ch in ner_interval:
        try:
            if len(ch) == 1:
                final_list.append(ch)
            elif len(ch) > 1:
                number_check_list = []
                complete_ner = ""
                for in_ in range(len(ch)):

                    try:
                        end_first_interval = ch[in_][1][1]
                        star_second_interval = ch[in_ + 1][1][0]
                        # print(ch[in_])
                        # print(ch[in_ + 1])
                        if star_second_interval == end_first_interval:
                            ner_char = [ch[in_][0], ch[in_ + 1][0]]
                            for e in ch[in_][1]:
                                number_check_list.append(e)
                            for k in ch[in_ + 1][1]:
                                number_check_list.append(k)
                            for char in ner_char:
                                if not char in complete_ner:
                                    complete_ner += (" " + char)
                        else:
                            if not number_check_list == []:
                                interval_ner = [min(number_check_list), max(number_check_list)]
                                final_list.append([complete_ner, interval_ner])
                                number_check_list = []
                    except Exception as e:
                        print("list finish")

        except Exception:
            print(Exception)
    print(final_list)
    return final_list
############------------***  EXTRACT ENTITY (NER)  ***-----------------##################
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

def get_entity(text):
    ner_model = build_model(configs.ner.ner_ontonotes_bert_torch, download=False)
    clean_text = text_cleaner(text)
    model = ner_model([clean_text[0]])
    ner = extract_entity(model)
    collapse_ner = collapse(ner)
    return collapse_ner

def split_by_sentence(text):
    doc = nlp(text)
    return doc.sents






