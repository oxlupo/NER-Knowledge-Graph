import re
import json
import pandas as pd
from cleaning.cleaner import css_cleaner
# from NER.NER import get_bert_dp_sub_token
# file_name = 'amazon.txt'
# text = open(f"text/{file_name}", 'r', encoding='utf-8')
# text = text.read()
# sentences_list = get_bert_dp_sub_token(file_path=f"text/{file_name}")
def get_raw_text(file_name):
    """return: the raw_text from file_name from json_files folder """
    data = open(file_name)
    file = json.load(data)
    raw_text_column = file["raw_text"]
    return raw_text_column

text = get_raw_text(file_name="json_files/amazon.json")
clean_text = css_cleaner(text)

print(clean_text)

