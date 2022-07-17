from cleaning.cleaner import word_tokenize
from NER.NER import get_entity

def text_interrupted(text):

    """This function display words in text in intervals type
     like [apple, [0, 1]]
     to make it easier to find relation between NER and verb"""
    clean_data = word_tokenize(text=text)
    list_ = []
    interval_word = []
    for index, token in enumerate(clean_data):

        interval = [token, [index, index + 1]]
        interval_word.append(interval)
    return interval_word

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
        if number_of_token >= 2:

            first_interval = []
            for interval in interval_word:

                for entity in token_list:
                    if entity == interval[0]:
                        first_interval.append(interval)
            check.append(first_interval)
        else:
            list_ = []
            for interval in interval_word:
                if token == interval[0]:
                    list_.append(interval)

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
    check_list = []
    ind = 0
    for ch in ner_interval:
        try:
            if len(ch) == 1:
                final_list.append(ch[0])
            elif len(ch) > 1:
                number_check_list = []
                complete_ner = ""
                for in_ in range(len(ch)):
                    try:
                        end_first_interval = ch[in_][1][1]
                        if not in_ == len(ch) - 1:
                            star_second_interval = ch[in_ + 1][1][0]
                        if star_second_interval == end_first_interval:
                            ner_char = [ch[in_][0], ch[in_ + 1][0]]
                            for e in ch[in_][1]:
                                number_check_list.append(e)
                            for k in ch[in_ + 1][1]:
                                number_check_list.append(k)
                            for char in ner_char:
                                if not char in complete_ner:
                                    complete_ner += (" " + char)
                            for element in [ch[in_], ch[in_ + 1]]:
                                if not element in check_list:
                                    check_list.append(element)
                        else:
                            if not number_check_list == []:
                                interval_ner = [min(number_check_list), max(number_check_list)]
                                final_list.append([complete_ner, interval_ner])
                                number_check_list = []

                    except Exception as e:
                        print(f"an error was appear in interval function:{e}")
                for element in ch:
                    if not element in check_list:

                        final_list.append(element)
        except Exception as e:
            print(e)
    print(final_list)
    return final_list
def optimize_interval(ner, text_interval):
    all_ = []
    ner_list = list(map(lambda x: x[0], ner))
    for ner in ner_list:
        for index, text in enumerate(text_interval):
            count_ner = len(ner.split(" "))
            if count_ner >= 2:
                ner_split = ner.split(" ")
                test_list = []
                interval_number = []
                for count in range(count_ner):
                    try:
                        test_list.append(text_interval[count + index][0])
                        for x in text_interval[count + index][1]:
                            interval_number.append(x)
                    except Exception as e:
                        continue
                join_text = " ".join(test_list)
                if ner == join_text:
                    ner_interval = [ner, [min(interval_number), max(interval_number)]]
                    print(ner_interval)
                    if not ner_interval in all_:
                        all_.append(ner_interval)
            else:
                for text in text_interval:
                    if ner == text[0]:
                        if not text in all_:
                            all_.append(text)
                            print(text)
    return all_

def find_ner_position(text_chunk, ner_list):
    """a function for finding the position of NER in text"""

    text_interval = text_interrupted(text=text_chunk)
    position_find = optimize_interval(ner=ner_list, text_interval=text_interval)

    return position_find

def find_ner_position_all_sentences(text_chunk, ner_list):
    """a function for finding the position of NER in text"""
    text = " ".join(text_chunk)
    text_interval = text_interrupted(text=text)
    position_find = optimize_interval(ner=ner_list, text_interval=text_interval)

    return position_find