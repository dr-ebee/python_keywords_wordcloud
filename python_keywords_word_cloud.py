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

def count_keywords():
    keyword_counter = Counter()

    def is_python_file(filename):
        return filename[-3:] == ".py"

    keyword_regex = f"\\b({'|'.join(keyword.kwlist)})\\b"

    def read_file_and_update_counter(filename):
        try:
            with open(filename) as f:
                content = f.read()
                # print(f"reading {filename}...")
                words = re.findall(keyword_regex, content)
                keyword_counter.update(words)
        except:
            pass

    root_dir = "/Users/erinbennett/Downloads/python-corpus/cleaned"

    def walk(dir, depth=0):
        if depth > 1:
            return
        subdirs = os.listdir(dir)
        for subdir in subdirs:
            filename = os.path.join(dir, subdir)
            if os.path.isdir(filename):
                walk(filename, depth = depth+1)
            elif is_python_file(filename):
                read_file_and_update_counter(filename)

    walk(root_dir)
    print(keyword_counter)

keyword_counter = {'if': 668419, 'in': 444107, 'def': 441969, 'for': 354337, 'return': 345347, 'import': 299904, 'and': 231973, 'not': 213646, 'None': 213204, 'is': 210602, 'from': 191930, 'else': 159122, 'True': 134425, 'False': 124164, 'or': 123727, 'with': 90966, 'as': 87376, 'class': 83658, 'elif': 79819, 'try': 79489, 'except': 77015, 'raise': 39473, 'pass': 30299, 'while': 25665, 'assert': 23208, 'continue': 20540, 'lambda': 19630, 'break': 17113, 'global': 13784, 'del': 10233, 'yield': 9149, 'finally': 6099, 'async': 584, 'nonlocal': 35, 'await': 19}

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
    relative_scaling = .1,
    font_path = font_path,
    mask=mask
    ).generate_from_frequencies(keyword_counter)

# create coloring from image
image_colors = ImageColorGenerator(mask)
plt.figure(figsize=[100,100])
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
plt.savefig("python_keywords.png", format="png")
plt.show()