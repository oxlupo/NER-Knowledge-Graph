import termcolor
from deeppavlov import configs, build_model
from collections import Counter
import pandas as pd
import json
re_model = build_model(configs.relation_extraction.re_docred, download=False)
# ner_list = [('Apple Inc.', 'ORG'), ('American', 'NORP'), ('Apple', 'ORG'), ('Apple', 'ORG'), ('Apple Park', 'FAC'), ('Cupertino', 'GPE'), ('California', 'GPE'), ('Apple', 'ORG'), ('1976', 'DATE'), ('Steve Wozniak', 'PERSON'), ('Steve Jobs', 'PERSON'), ('Ron Wayne', 'PERSON'), ('first', 'ORDINAL'), ('Apple', 'ORG'), ('Lisa', 'PRODUCT'), ('Macintosh', 'PRODUCT'), ('iPod', 'PRODUCT'), ('2001', 'DATE'), ('iPhone', 'PRODUCT'), ('2007', 'DATE'), ('iPad', 'PRODUCT'), ('2010', 'DATE'), ('Apple', 'ORG'), ('day', 'DATE'), ('recent years', 'DATE'), ('iPhone', 'PRODUCT'), ('Apple', 'ORG'), ('50 %', 'PERCENT'), ('iTunes', 'ORG'), ('2003', 'DATE'), ('first', 'ORDINAL'), ('Today', 'DATE'), ('iTunes Store App Store', 'ORG'), ('2008', 'DATE'), ('two', 'CARDINAL')]
# ner_list = [[('Kala Sepid Tarabar | International Transport Company', 'ORG'), ('Tehran', 'GPE'), ('Iran', 'GPE'), ('98', 'CARDINAL'), ('21', 'CARDINAL'), ('Contact Gallery International Transportation & Trading Company', 'ORG'), ('Asia', 'LOC'), ('Europe', 'LOC'), ('KALA SEPID TARABAR', 'ORG'), ('Kala', 'GPE'), ('four', 'CARDINAL'), ('International Transportation & Trading Company', 'ORG'), ('Iran International Transportation & Trading Company', 'ORG'), ('Iran', 'GPE'), ('Mashhad International Logistic Company International Logistic Company', 'ORG'), ('Iran', 'GPE'), ('Mashhad', 'GPE'), ('Kala Sepid Tarabar International Transport Company', 'ORG'), ('Asia', 'LOC'), ('Kala Sepid Tarabar', 'ORG'), ('four', 'CARDINAL'), ('/ /', 'CARDINAL'), ('365', 'CARDINAL'), ('5', 'CARDINAL'), ('24 hours', 'TIME'), ('Iranian', 'NORP'), ('CIS', 'LOC'), ('China', 'GPE'), ('Jebel', 'GPE'), ('Guangzhou', 'GPE'), ('Iran', 'GPE')], [('first', 'ORDINAL'), ('HAPPY NOWRUZ', 'EVENT'), ('March 19 , 2022 Day', 'DATE'), ('March 8 , 2022', 'DATE'), ('Happy Chinese New Year', 'EVENT'), ('February 1 , 2022', 'DATE'), ('January 13 , 2022', 'DATE'), ('Merry Christmas Happy New Year', 'EVENT'), ('December 23 , 2021', 'DATE'), ('Sajjad Abyar', 'PERSON'), ('Meshkat Palm', 'ORG'), ('year', 'DATE'), ('Mohammad Reza Barakchian', 'PERSON'), ('Amoot Iranian KST International Transport Company', 'ORG'), ('KST', 'ORG'), ('Hesham Hoseini', 'PERSON'), ('Pars Tarabar About Us', 'ORG'), ('Kala Sepid Tarabar International Transportation Company', 'ORG'), ('20 years', 'DATE'), ('HAPPY NOWRUZ', 'EVENT'), ('March 19 , 2022 Day', 'DATE'), ('March 8 , 2022', 'DATE'), ('KST International Transport Company', 'ORG'), ('Iran', 'GPE'), ('Afghanistan', 'GPE'), ('Turkey', 'GPE'), ('Turkmenistan', 'GPE'), ('Uzbekistan', 'GPE'), ('Tajikistan', 'GPE'), ('China', 'GPE'), ('U', 'GPE'), ('.', 'GPE'), ('S', 'GPE'), ('.', 'GPE'), ('A', 'GPE'), ('.', 'GPE'), ('U', 'GPE'), ('.', 'GPE'), ('A', 'GPE'), ('.', 'GPE'), ('E', 'GPE'), ('.', 'GPE'), ('Dubai', 'GPE'), ('Kala Sepid Tarabar', 'PERSON')]]
data = open('check.json', 'r')
check_json = json.load(data)

def entity_tag(ner_list, entity_):
    """for get better accuracy for relation extraction
     we need to get type of entity for related to main entity """
    entity = entity_[0].strip()
    try:
        for ner in ner_list:
            if entity in ner:
                return ner[1]
    except Exception as e:
        print("THE NER DOSEN'T EXIST IN NER_LIST")
        return None

def make_standard_list(entity_position):
    """sometimes the list in interval step dosen't"""
    ent_list = []
    for pos in entity_position:
        if pos.index() == 1:
            ent_list.append(pos[0])
    return ent_list

def pair_entity_type(entity_type):
    """convert type of NER model --> to relation extraction model type"""

    if entity_type == "PERSON":
        return "PER"
    elif entity_type == "ORG":
        return "ORG"
    elif entity_type == "LOC" or entity_type == "GPE" or entity_type == "FAC":
        return "LOC"
    elif entity_type == "TIME" or entity_type == "DATE":
        return "TIME"
    elif entity_type == "QUANTITY" or entity_type == "MONEY" or entity_type == "PERCENT":
        return "NUM"
    elif entity_type == "PRODUCT" or entity_type == "LANGUAGE" or entity_type == "LAW":
        return "MISC"
    else:
        return "OTHER"


def most_org_repetition_interval(ner_list, entity_position):
    """a function for get the most common ORG that iterate in text get it for main ORG of text"""

    most_org = []
    org = []
    ner = list(filter(lambda x: org.append(x[0]) if x[1] == "ORG" else False, ner_list))
    counter = Counter(org)
    most_common = counter.most_common(1)
    most_org.append(most_common)

    return most_org
def calculate_accuracy(true, count):
    accuracy = (true / count) * 100
    return accuracy
def pair_most_common_and_entity(entity, most_org):
    """this function find the interval of the most organization that repeat in text"""

    pair_most_common = []
    tuple_most_pair = []

    for ent in entity:
        if most_org[0][0][0] == ent[0]:
            if pair_most_common == []:
                pair_most_common.append(ent[1])
    for e in pair_most_common:
        e = tuple(e)
        tuple_most_pair.append(e)
    return tuple_most_pair

def get_relation(sentence_tokens, entity_position, ner_list):
    """ a function for find relation between central ORG and other NER """

    relation_list = []
    source_list = []
    target_list = []
    check_ner_list = []
    most_common = most_org_repetition_interval(ner_list, entity_position)
    pair_most_common = pair_most_common_and_entity(entity_position, most_org=most_common)
    count = 0
    true = 0
    for pos in entity_position:
        tag = entity_tag(ner_list=ner_list, entity_=pos)  # ORG for example
        paired = pair_entity_type(entity_type=tag)
        if paired == "OTHER":
            continue
        if pos[0].strip() == most_common[0][0][0].strip():
            continue
        ner_position = tuple(pos[1])
        ner = pos[0]
        if ner in check_ner_list:
            continue
        check_ner_list.append(ner)
        entity_pos = [[[pair_most_common[0]], [ner_position]]]
        # entity_pos = [[[(73, 74)], [ner_position]]]
        try:
            entity_tags = [["ORG", paired]]
            prediction = re_model(sentence_tokens, entity_pos, entity_tags)
            if ner in check_json.keys():
                if "/" in check_json[ner]:
                    products = check_json[ner].split("/")
                    if prediction[1][0] in products:
                        count += 1
                        true += 1
                    else:
                        count += 1
                else:
                    if prediction[1][0] == check_json[ner]:
                        count += 1
                        true += 1
                    else:
                        count += 1
            print(termcolor.colored(str(most_common[0][0][0] + " " + ">>>>>>>>>>" + " " + str(prediction[1]) + " " + ">>>>>>>>>>" + " " + ner + " " +paired), "green"))
        except Exception as e:
            print(e)
        source_list.append(str(most_common[0][0][0]))
        relation_list.append(prediction[1][0])
        target_list.append(ner)
    try:
        accuracy = calculate_accuracy(true, count)
    except Exception:
        accuracy = "non of specific NER wasn't in text"
    print(f"accuracy:", {accuracy})
    kg_df = pd.DataFrame({'source': source_list, 'edge': relation_list, 'target': target_list})
    return [kg_df, accuracy]
def get_relation_between_sentences_ner(sentence_tokens, entity_position, ner_list):

    relation_list = []
    source_list = []
    target_list = []
    check = []
    count = 0
    true = 0
    for ner in entity_position:
        try:
            for target in entity_position:
                if ner[0] == target[0]:
                    continue
                ner_name = ner[0]
                target_name = target[0]
                check_list = tuple([ner_name, target_name])
                tag_ner = entity_tag(ner_list=ner_list, entity_=ner)
                tag_target = entity_tag(ner_list=ner_list, entity_=target)
                paired_ner = pair_entity_type(entity_type=tag_ner)
                paired_target = pair_entity_type(entity_type=tag_target)
                if paired_ner == "OTHER":
                    continue
                elif paired_target == "OTHER":
                    continue
                elif check_list in check:
                    continue
                check.append(check_list)
                ner_position = tuple(ner[1])
                target_position = tuple(target[1])
                entity_pos = [[[ner_position], [target_position]]]
                try:
                    entity_tags = [[paired_ner, paired_target]]
                    prediction = re_model(sentence_tokens, entity_pos, entity_tags)
                except Exception as e:
                    print(e)
                print(termcolor.colored(str(ner[0] + " " + ">>>>>>>>>>" + " " + str(prediction[1]) + " " + ">>>>>>>>>>" + " " + target_name + " " + f"({tag_ner}, {tag_target})"), "green"))
                source_list.append(str(ner_name))
                relation_list.append(prediction[1][0])
                target_list.append(target_name)
                try:
                    accuracy = calculate_accuracy(true, count)
                except Exception:
                    accuracy = "in the next steps add this feature"
                print(f"accuracy:", {accuracy})
        except Exception as e:
            print(e)
            continue
    kg_df = pd.DataFrame({'source': source_list, 'edge': relation_list, 'target': target_list})
    accuracy = 0
    return [kg_df, accuracy]