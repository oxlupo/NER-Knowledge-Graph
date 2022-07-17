import json
import requests
# from warcio import ArchiveIterator
from pymongo import MongoClient
import wget
import urllib.request
import gzip
# import shutil
# import os
from termcolor import colored
import random
from bson.objectid import ObjectId
import multiprocessing
from deeppavlov import configs, build_model
import cdx_toolkit
import time
from product import extract_product_html
ner_model = build_model(configs.ner.ner_ontonotes_bert_torch, download=False)

COLLECTION_PHONE = 'Phones'
COLLECTION_EMAIL = 'Emails'
COLLECTION_LINKEDIN = 'Linkedin'
COLLECTION_FACEBOOK = 'Facebook'
COLLECTION_TWITTER = 'Twitter'
COLLECTION_YOUTUBE = 'Youtube'
COLLECTION_INSTAGRAM = 'Instagram'

##############################################################
client = MongoClient('localhost', 27017, maxPoolSize = 500)
db = client.Linkedin
collection_boobranda_total_cleaned = db['urls_05_2022_2']
collection_website_unique = db['linkedin_only_website_unique']

collection_phone = db[COLLECTION_PHONE]
collection_email = db[COLLECTION_EMAIL]
collection_linkedin = db[COLLECTION_LINKEDIN]
collection_facebook = db[COLLECTION_FACEBOOK]
collection_twitter = db[COLLECTION_TWITTER]
collection_youtube = db[COLLECTION_YOUTUBE]
collection_instagram = db[COLLECTION_INSTAGRAM]
##############################################################

def gunzip(source_filepath, dest_filepath, block_size=65536):
    with gzip.open(source_filepath, 'rb') as s_file, \
            open(dest_filepath, 'wb') as d_file:
        while True:
            block = s_file.read(block_size)
            if not block:
                break
            else:
                d_file.write(block)

def check_root_url(url):

    if ( url== None ):
        return False

    url = url.strip()
    url = url.replace('http://', '')
    url = url.replace('https://', '')
    url = url.replace('www.', '')
    if (url.endswith('/')):
        url = url[:-1]
    if (len(url.split('/')) == 1):
        return True
    else:
        return False

def check_contact_url(url):
    if ( url== None ):
        return False

    if ('contact' in url.lower()):
        return True
    else:
        return False

def verify_social_url (url,  valid_part):
    try:
        url = url.replace('www.','').replace('http://','').replace('https://','')
        while url.endswith('/'):
            url = url[:-1]
        split_list = url.split('/')
        if (len(split_list) == valid_part):
            return True
    except Exception as e:
        print(e)
        return False

    return False

def insert_phone_mongo (phone, url):
    try:
        insertJson ={'phone': phone, 'url': url}
        collection_phone.insert_one(insertJson)
    except Exception as e:
        print(e)

def insert_email_mongo (email, url):
    try:
        domain = email.split('@')[-1]
        insertJson ={'email': email, 'url': url, 'domain': domain.strip()}
        collection_email.insert_one(insertJson)
    except Exception as e:
        print(e)

def insert_phone_mongo (phone, url):
    try:
        insertJson ={'phone': phone, 'url': url}
        collection_phone.insert_one(insertJson)
    except Exception as e:
        print(e)

def insert_linkedin_mongo (linkedin, url):
    try:
        insertJson ={'linkedin': linkedin, 'url': url}
        collection_linkedin.insert_one(insertJson)
    except Exception as e:
        print(e)

def insert_facebook_mongo (facebook, url):
    try:
        insertJson ={'facebook': facebook, 'url': url}
        collection_facebook.insert_one(insertJson)
    except Exception as e:
        print(e)

def insert_twitter_mongo (twitter, url):
    try:
        insertJson ={'twitter': twitter, 'url': url}
        collection_twitter.insert_one(insertJson)
    except Exception as e:
        print(e)

def insert_youtube_mongo (youtube, url):
    try:
        insertJson ={'youtube': youtube, 'url': url}
        collection_youtube.insert_one(insertJson)
    except Exception as e:
        print(e)

def insert_instagram_mongo (instagram, url):
    try:
        insertJson ={'instagram': instagram, 'url': url}
        collection_instagram.insert_one(insertJson)
    except Exception as e:
        print(e)

def get_from_mongo_url():

    category = collection_boobranda_total_cleaned.find_and_modify(query={'tag': False}, update={'$set': {"tag": 'progress'}})
    return category

def get_from_url():

    return {'website': 'microsoft.com/en-us'}
    while True:
        try:
            category = collection_website_unique.find_and_modify(query={'tag': False}, update={'$set': {"tag": 'progress'}})
            return category
        except Exception as e:
            print(e)
            time.sleep(10)

def update_mongo_url(id):
    collection_boobranda_total_cleaned.find_and_modify(query={'_id': ObjectId(id)}, update={'$set': {"tag": True}})



def get_html_cdx_toolkit(url):

    while True:

        try:
            cdx = cdx_toolkit.CDXFetcher(source='cc')

            #
            for obj in cdx.iter(url, limit=1):
                try:
                    if (obj.content != None and obj.content != ''):
                        return obj.content
                except Exception as e:
                    continue
            return ''

        except Exception as e:
            print(e)


def a():
    item = get_from_url()

    while True:

        if item == None:
            time.sleep(20*1)
            print(colored(' sleep !!!!' , 'magenta'))
            item = get_from_url()

            continue


        url = item['website']
        contents = get_html_cdx_toolkit(url)

        if (contents == ''):
            product_list = []

            continue

        print(colored(' produce ' + str(url) + ' started !', 'green'))

        product_list = extract_product_html(contents)




        if (product_list != []):
            insert_instagram_mongo(product_list, url)


        item = get_from_url()

###############################################################################


number_processes = 1
processes = []

for i in range(number_processes):
    processes.append(multiprocessing.Process(target=a, args=[]))

for index, p in enumerate(processes):
    p.start()

for index, p in enumerate(processes):

    p.join()

