import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from collections import Counter
from nltk import ngrams
import heapq


def get_ngrams(words, n):
    return list(ngrams(words, n))


def remove_specific_pair(lst, first, second='', third='', fourth=''):
    if (second == ''):
        i = 0
        while i < len(lst) - 1:
            if lst[i] == first:
                del lst[i]
            else:
                i += 1
    elif (third == ''):
        i = 0
        while i < len(lst) - 1:
            if lst[i] == first and lst[i + 1] == second:
                del lst[i + 1]
                del lst[i]
            else:
                i += 1
    else:
        if (fourth == ''):
            i = 0
            while i < len(lst) - 2:
                if lst[i] == first and lst[i + 1] == second and lst[i + 2] == third:
                    del lst[i + 2]
                    del lst[i + 1]
                    del lst[i]
                else:
                    i += 1
        else:
            i = 0
            while i < len(lst) - 3:
                if lst[i] == first and lst[i + 1] == second and lst[i + 2] == third and lst[i + 3] == fourth:
                    del lst[i + 3]
                    del lst[i + 2]
                    del lst[i + 1]
                    del lst[i]
                else:
                    i += 1
    return lst


def replace_numbers_and_special_characters(text):
    return re.sub(r'[^a-zA-Z\s]', '', text)


def remove_word(word):
    if word == 'vcb':
        return False
    if word == 'ct':
        return False
    if word == 'vietcombank':
        return False
    if word == 'mbvcb':
        return False
    if word == 'ctdk':
        return False
    if word == 'jdc':
        return False
    if word == 'mhs':
        return False
    if word == 'zj':
        return False
    if word == 'qws':
        return False
    if word == 'mbvcb':
        return False
    if word == 'tw':
        return False
    if word == 'a':
        return False
    if word == 'elg':
        return False
    return True


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    text = replace_numbers_and_special_characters(text)
    words = text.split()
    return words


def format_number(num):
    if num >= 1_000_000_000_000:
        return f'{num / 1_000_000_000_000:.1f}T'
    if num >= 1_000_000_000:
        return f'{num / 1_000_000_000:.1f}B'
    elif num >= 1_000_000:
        return f'{num / 1_000_000:.1f}M'
    elif num >= 1_000:
        return f'{num / 1_000:.1f}K'
    else:
        return str(num)


directory = 'chart/vcb'
if not os.path.exists(directory):
    os.makedirs(directory)

fileOutput = 'output/vcb.xlsx'
df = pd.read_excel(fileOutput)

text = " ".join(df['message'])
words = preprocess_text(text)

max = 10
for num in range(1, 5):
    print(f"Group: {num}")
    ngrams_words = get_ngrams(words, num)
    ngrams_counts = Counter(ngrams_words)
    top = heapq.nlargest(max, ngrams_counts.items(), key=lambda x: x[1])
    top_counter = Counter(dict(top))
    # other_count = sum((ngrams_counts - top_counter).values())
    # top_counter['other'] = other_count
    labels = list()
    values = list()
    for key, value in top_counter.items():
        if (key == 'other'):
            capitalized = key.capitalize()
        else:
            capitalized = " ".join([word.capitalize() for word in key])
        labels.append(capitalized)
        values.append(value)
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    plt.subplots_adjust(left=0.2)
    bars = plt.barh(labels, values)
    for bar in bars:
        value = f'{format_number(bar.get_width())}'
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() /
                 2, value, va='center', ha='left')
    plt.xlabel(f'Tần suất')
    plt.ylabel('Từ')
    plt.title('Biểu đồ tần suất xuất hiện từ')
    plt.savefig(f'{directory}/word_{num}_trending.png')
