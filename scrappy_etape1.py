import os
import stat
import requests
from bs4 import BeautifulSoup
from pathlib 
import csv
import time
from slugify import slugify
import urllib.request

#random sleep mode
min_sleep = 1
max_sleep =3

#before we start we need  to remove scrappy
shutil.rmtree("")