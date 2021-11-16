import os
import stat
import random
from typing import Mapping
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import shutil
import csv
import time
from requests.models import Response
from slugify import slugify
import urllib.request
import re

# random sleep mode
MIN_SLEEP = 1
MAX_SLEEP = 3

# remove scrappy before restart
shutil.rmtree('./scrappy', ignore_errors=True)

def progressBar(iterable, prefix = "", suffix = '',decimals = 1, length = 100, fill = '█', printEnd= '\r'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar printing fUNCTION
    def printProgressBar(iteration):
        percent = ("{0:." + 
        str(decimals) + 
        "f})").format(100 * iteration / float(total))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length) - filledLength)
        print(f'\r{prefix} | {bar}|{percent}%{suffix}', end = printEnd)
    #Initail Call
    printProgressBar(0)
    #update Progress Bar
    for i,item in enumerate(iterable):
        yield item
        printProgressBar(i+1)
    #Print New line empty on compile
    print()

def scrappy_product_category(soup):
    links = []

    products = soup.select('article.product_pod')

    for product in products:
        href = product.find('a')['href']
        href = href.split('/')
        links.append("http://books.toscrape.com/catalogue/" + href[-2] + "/" + href[-1])
    return links


def find_product_url_by_category(url_categ):
    #produit par page  : 20
    response = requests.get(url_categ)
    links = []

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')

        is_pagination = soup.find('ul', {"class": 'pager'})
        if is_pagination:
            nbPages:
            for i in range(1,nbPages+1):
                url = url_categ.replace('index.html','page-'+str(i)+'.html')
                response = requests.get(url)
                if(response.ok):
                    soup = BeautifulSoup(response.text, 'html.parser')
                    links = links + scrappy_product_category(soup)
                # Eviter l' IP  blacklistee
                time.sleep(random.uniform(MIN_SLEEP,MAX_SLEEP))
        else:
            links = scrappy_product_category(soup)
    return links


def scrappy_product(url, upload_image, slug_categ):
    product_informations = {
        "product_page_url": url
    }

    response = requests.get(product_informations["product_page_url"])

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Recuperer universal_product_code / price_excluding_tax / price_including_tax(tableau d'information en bas de page de produit)
        informations = soup.findAll("tr")

        for information in informations:
            information_label = information.find('th').text
            information_value = information.find('td').text
            
            target_dict = False
            if (information_label == "UPC"):
                target_dict = "universal_product_code"
            elif (information_label == "Price (excl. tax)"):
                target_dict = "price_excluding_tax"
            elif (information_label == "Price (incl. tax)"):
                target_dict = "price_including_tax"

            if target_dict:
                if "Â" in information_value:
                    information_value = information_value.replace("Â", "")

                product_informations[target_dict] = information_value






