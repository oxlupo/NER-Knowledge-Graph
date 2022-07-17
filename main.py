import termcolor
from NER.NER import get_entity, split_by_sentence, get_bert_dp_sub_token
from cleaning.clean_text import *
from cleaning.cleaner import tokenize_word, split_text_by_token, tokenize_word_all_sentences
from cleaning.interval import find_ner_position, find_ner_position_all_sentences
from NER.relation_extraction import get_relation, most_org_repetition_interval, get_relation_between_sentences_ner
from connection import connection, specifictag
from plot.plot import visualize_graph
from bs4 import BeautifulSoup as soup
file_name = 'apple.txt'
text = open(file_name, 'r', encoding='utf-8')
text = text.read()

# text = connection(url="https://www.ryerson.ca/programs/undergraduate/computer-engineering/#Academic-Requirements")
sentences_list = get_bert_dp_sub_token(file_path=file_name)
# clean_text = text_cleaner(text)
# tokenize_sentences = tokenize_word(text)
# split_by_512_chunk = split_text_by_token(text)


def sentence_by_sentence(sentences_list):
    for sentences in sentences_list:
        try:
            tokenize_sentences = tokenize_word(text=sentences)
            ner_list = split_by_sentence(sentences=sentences_list)
            print(termcolor.colored(ner_list, "green"))
            entity_pos = find_ner_position(text_chunk=sentences, ner_list=ner_list)
            # relation = get_relation_between_sentences_ner(sentence_tokens=tokenize_sentences, entity_position=entity_pos, ner_list=ner_list)
            relation = get_relation(sentence_tokens=tokenize_sentences, entity_position=entity_pos, ner_list=ner_list)
            visualize_graph(relation[0], accuracy=relation[1])
        except Exception as e:
            print(e)

def all_text_in_one(sentences_list):
    try:
        clean_text = text_cleaner(text)
        # tokenize_sentences = tokenize_word(clean_text)
        split_by_512_chunk = split_text_by_token(clean_text)
        tokenize_sentences = tokenize_word_all_sentences(sentences_list)
        ner_list = split_by_sentence(sentences=split_by_512_chunk)
        print(termcolor.colored(ner_list, "green"))
        entity_pos = find_ner_position_all_sentences(text_chunk=split_by_512_chunk, ner_list=ner_list)
        relation = get_relation(sentence_tokens=tokenize_sentences, entity_position=entity_pos, ner_list=ner_list)
        visualize_graph(relation[0], accuracy=relation[1])
    except Exception as e:
        print(e)
# all_text_in_one(sentences_list)
sentence_by_sentence(sentences_list)