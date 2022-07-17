from deeppavlov import configs, build_model
from cleaning.cleaner import text_cleaner
import spacy
nlp = spacy.load("en_core_web_sm")
ner_model = build_model(configs.ner.ner_ontonotes_bert_torch, download=False)
from bert_dp.tokenization import FullTokenizer


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


def get_bert_dp_sub_token(file_path):
    tokenizer = FullTokenizer(vocab_file=file_path, do_lower_case=False)
    sentences = tokenizer.inv_vocab.values()
    sentences_list = list(map(lambda x: str(x), sentences))
    return sentences_list


def split_by_sentence(sentences):
    """this function for split text by sentences"""
    list_ = []
    final_list = []
    try:
        model = ner_model([str(sentences)])
        ner = extract_entity(model)
        collapse_ner = collapse(ner)
        list_.append(collapse_ner)
    except Exception as e:
        print(e)
    for list__ in list_:
        for ner in list__:
            if not ner[0] == "," or ner[0] == '.':
                final_list.append(ner)

    return final_list


def get_entity(text_list):
    """get all entity from text with bert-model"""
    list_ = []
    for chunk in text_list:
        model = ner_model([chunk])
        ner = extract_entity(model)
        collapse_ner = collapse(ner)
        list_.append(collapse_ner)
    final_list = []
    for ner in list_:
        for n in ner:
            if not n[0] == "," or n[0] == '.':
                final_list.append(n)
    return final_list



