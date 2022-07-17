from NER import get_entity
from cleaning.cleaner import *
from connection import connection
from relation_extraction import most_org_repetition_interval
import pandas as pd
import os
import termcolor
from bs4 import BeautifulSoup

csv_file = pd.read_csv("US B2b Linkedin Part 1.csv")

Email = csv_file['Email'].values
Company = csv_file['Company'].values
Web_site = list(map(lambda x: "https://"+x.split("@")[1], Email))

company_detail = list(map(lambda x, y, z: [x, y, z], Email, Company, Web_site))
data = []
for website in os.listdir("text"):
    try:
        list_ = []
        text = connection(url=website[2])
        # data1 = specifictag(url="https://www.armaninollp.com")
        soup = BeautifulSoup(text, "html.parser")
        text = soup.text
        # sents = list(split_by_sentence(text=data1))

        clean_text = text_cleaner(str(text))
        tokenize_sentences = tokenize_word(clean_text)
        split_by_512_chunk = split_text_by_token(clean_text)
        ner_list = get_entity(text_list=split_by_512_chunk)

        print(termcolor.colored(ner_list, "green"))
        most_org = most_org_repetition_interval(ner_list=ner_list, entity_position="NEED")
        # list_.append(most_org)

        if most_org == [[]]:
            website.append("NOT FOUND")
            data.append(website)
        else:
            website.append(most_org[0][0][0])
            data.append(website)
    except Exception as e:
        # website.append(f"GOT AN EXCEPTION")
        # data.append(website)
        print(e)

Email = [x[0] for x in data]
Company = [x[1] for x in data]
Web_site = [x[2] for x in data]
Org_find = [x[3] for x in data]

data_frame = pd.DataFrame({
    "Email": Email,
    "Company": Company,
    "Website": Web_site,
    "ORG Find": Org_find
})
data_frame.to_csv("most_org_sent2.csv", index=False)

# text = connection(url="https://kst-transportation.com")
# clean_text = text_cleaner(text)
#
# tokenize_sentences = tokenize_word(clean_text)
# split_by_512_chunk = split_text_by_token(clean_text)
#
# ner_list = get_entity(text_list=split_by_512_chunk)
# all_ner_in_one = []
# for ner in ner_list:
#     all_ner_in_one.extend(ner)
#
# most_ORG = most_org_repetition_interval(ner_list=ner_list, entity_position="ORG")
#
# print(colored(text=most_ORG, color='green'))

