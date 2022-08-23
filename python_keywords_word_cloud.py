from ast import keyword
from pydoc import ispackage
import pandas as pd
import re
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
from time import sleep
from random import random
import os
import glob
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import matplotlib.colors as clr
import keyword
from collections import Counter
import pickle

keyword_list = keyword.kwlist
punct_list = []#["\\[", "\\]", "{", "}", ":", "\\(", "\\)"]

def count_keywords():
    keyword_counter = Counter()

    def is_python_file(filename):
        return filename[-3:] == ".py"

    keyword_regex = f"\\b({'|'.join(keyword_list)})\\b"
    punct_regex = f"({'|'.join(punct_list)})"

    def read_file_and_update_counter(filename):
        try:
            with open(filename) as f:
                content = f.read()
                # print(f"reading {filename}...")
                words = re.findall(keyword_regex, content)
                punct = re.findall(punct_regex, content)
                keyword_counter.update(words)
                keyword_counter.update(punct)
        except:
            pass

    root_dir = "/Users/erinbennett/Downloads/python-corpus/cleaned"

    def walk(dir, depth=0):
        if depth > 20:
            return
        subdirs = os.listdir(dir)[:200]
        for subdir in subdirs:
            filename = os.path.join(dir, subdir)
            if os.path.isdir(filename):
                walk(filename, depth = depth+1)
            elif is_python_file(filename):
                read_file_and_update_counter(filename)

    walk(root_dir)
    print(keyword_counter)
    return keyword_counter

# keyword_counter = count_keywords()
# keyword_counter = {'if': 668419, 'in': 444107, 'def': 441969, 'for': 354337, 'return': 345347, 'import': 299904, 'and': 231973, 'not': 213646, 'None': 213204, 'is': 210602, 'from': 191930, 'else': 159122, 'True': 134425, 'False': 124164, 'or': 123727, 'with': 90966, 'as': 87376, 'class': 83658, 'elif': 79819, 'try': 79489, 'except': 77015, 'raise': 39473, 'pass': 30299, 'while': 25665, 'assert': 23208, 'continue': 20540, 'lambda': 19630, 'break': 17113, 'global': 13784, 'del': 10233, 'yield': 9149, 'finally': 6099, 'async': 584, 'nonlocal': 35, 'await': 19}
# keyword_counter = {'(': 328941, ')': 328791, ':': 302851, '[': 85702, ']': 85641, 'if': 43764, 'def': 37034, 'in': 32232, '{': 32192, '}': 31995, 'return': 28428, 'for': 25703, 'is': 22505, 'None': 21778, 'and': 19627, 'import': 19003, 'not': 18475, 'from': 14480, 'class': 11779, 'True': 11607, 'or': 11174, 'else': 10711, 'False': 8925, 'as': 8238, 'with': 7976, 'elif': 4915, 'raise': 4830, 'try': 4823, 'except': 4384, 'pass': 2425, 'assert': 2025, 'lambda': 1302, 'continue': 1300, 'while': 1233, 'yield': 1156, 'break': 1144, 'del': 792, 'finally': 577, 'global': 542, 'async': 40, 'await': 5, 'nonlocal': 4}
keyword_counter = {'if': 51894, 'def': 46459, 'in': 37405, 'return': 34773, 'for': 30030, 'None': 27524, 'True': 27442, 'import': 26643, 'is': 25799, 'and': 22194, 'not': 21752, 'from': 20541, 'class': 14971, 'or': 12702, 'else': 12606, 'False': 12599, 'as': 9588, 'with': 9131, 'try': 6284, 'raise': 5982, 'except': 5972, 'elif': 5900, 'pass': 3024, 'assert': 2430, 'while': 1534, 'lambda': 1512, 'continue': 1506, 'yield': 1421, 'break': 1386, 'del': 993, 'global': 718, 'finally': 649, 'async': 77, 'await': 8, 'nonlocal': 4}

# Generate a word cloud image
image_mask_file = "python_logo.png"
# image_mask_file = "python_logo_solid.png"
# image_mask_file = "flourish_square.png"
# image_mask_file = "kehillah_logo.png"
# image_mask_file = "flourish circle blue.png"
# image_mask_file = "flourish only.png"
mask = np.array(Image.open(image_mask_file))

font_path = "brandon-grotesque-black-58a8a3e824392.otf"

# generating word cloud
wordcloud = WordCloud(
    background_color="white", 
    mode="RGB", 
    max_words=100,
    relative_scaling = .3,
    font_path = font_path,
    mask=mask
    ).generate_from_frequencies(keyword_counter)

# create coloring from image
image_colors = ImageColorGenerator(mask)
plt.figure(figsize=[5,5])
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
plt.tight_layout(pad=.1)
plt.axis("off")
plt.savefig("python_keywords.png", format="png")
plt.show()

""