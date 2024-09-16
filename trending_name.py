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
    lst = lst.split()
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
    return " ".join(lst)


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
    if word == 'bao':
        return False
    if word == 'dong':
        return False
    if word == 'lu':
        return False
    if word == 'tu':
        return False
    if word == 'vn':
        return False
    if word == 'toi':
        return False
    if word == 'yagi':
        return False
    if word == 'ft':
        return False
    if word == 'khac':
        return False
    if word == 'lut':
        return False
    if word == 'con':
        return False
    if word == 'bi':
        return False
    if word == 'qua':
        return False
    if word == 'ho':
        return False
    if word == 'tro':
        return False
    if word == 'so':
        return False
    if word == 'do':
        return False
    if word == 'nguoi':
        return False
    if word == 'transactions':
        return False
    if word == 'detail':
        return False
    if word == 'cac':
        return False
    if word == 'vung':
        return False
    if word == 'tinh':
        return False
    if word == 'chuyen':
        return False
    if word == 'cuu':
        return False
    if word == 'thien':
        return False
    if word == 'tai':
        return False
    if word == 'se':
        return False
    if word == 'partner':
        return False
    if word == 'directdebitsvcb':
        return False
    if word == 'mse':
        return False
    if word == 'chia':
        return False
    if word == 'co':
        return False
    if word == 'xin':
        return False
    if word == 'ba':
        return False
    if word == 'thiet':
        return False
    if word == 'mong':
        return False
    if word == 'ni':
        return False
    if word == 'in':
        return False
    if word == 'tit':
        return False
    if word == 'chi':
        return False
    return True


def clean_message(text):
    text = text.lower()
    text = replace_numbers_and_special_characters(text)
    text = remove_specific_pair(text, 'mat', 'tran', 'to', 'quoc')
    text = remove_specific_pair(text, 'ban', 'cuu', 'tro')
    text = remove_specific_pair(text, 'chuyen', 'tien')
    text = remove_specific_pair(text, 'ung', 'ho')
    text = remove_specific_pair(text, 'vn', 'tw')
    text = remove_specific_pair(text, 'ct', 'tu')
    text = remove_specific_pair(text, 'mat', 'tran')
    text = remove_specific_pair(text, 'to', 'quoc')
    text = remove_specific_pair(text, 'mien', 'bac')
    text = remove_specific_pair(text, 'mien', 'nam')
    text = remove_specific_pair(text, 'viet', 'nam')
    text = remove_specific_pair(text, 'binh', 'an')
    text = text.split()
    text = list(filter(lambda x: remove_word(x), text))
    return " ".join(text)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
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

df['message'] = df['message'].apply(clean_message)
text = " ".join(df['message'])
words = preprocess_text(text)

max = 10
top_counter = Counter(words).most_common(max)
labels, values = zip(*top_counter)
labels = [label.capitalize() for label in labels]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(labels, values, width=0.8)
for bar in bars:
    height = bar.get_height()
    value = f'{format_number(height)}'
    ax.text(bar.get_x() + bar.get_width() / 2,
            height, value, ha='center', va='bottom')

plt.title('Thống kê theo Họ/Tên')
plt.xticks(rotation=90)
plt.ylabel('Tổng hợp giao dịch')
plt.ylim(bottom=0.1)
plt.savefig(f'{directory}/name_sum.png')