import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from collections import Counter
from nltk import ngrams


def get_ngrams(words, n):
    return list(ngrams(words, n))


def remove_specific_pair(lst, first, second, third='', fourth=''):
    if (third == ''):
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
    words = list(filter(lambda x: remove_word(x), words))
    words = remove_specific_pair(words, 'mat', 'tran', 'to', 'quoc')
    words = remove_specific_pair(words, 'ban', 'cuu', 'tro')
    words = remove_specific_pair(words, 'chuyen', 'tien', 'tu')
    words = remove_specific_pair(words, 'chuyen', 'tien')
    words = remove_specific_pair(words, 'tu', 'toi')
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
df['issue_date'] = pd.to_datetime(df['issue_date'])
df['issue_date'] = df['issue_date'].dt.strftime('%d/%m')

df_sum_daily = df.groupby(df['issue_date'])['amount'].sum().reset_index()
df_sum_daily.columns = ['date', 'value']

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(df_sum_daily['date'], df_sum_daily['value'], width=0.8)
for bar in bars:
    height = bar.get_height()
    value = f'{format_number(height)}'
    ax.text(bar.get_x() + bar.get_width() / 2,
            height, value, ha='center', va='bottom')

plt.title('Tổng số tiền theo từng ngày')
plt.xticks(rotation=90)
plt.ylabel('Tổng số tiền')
plt.ylim(bottom=0.1)
plt.savefig(f'{directory}/daily_sum.png')

df_count_daily = df.groupby(df['issue_date'])['amount'].count().reset_index()
df_count_daily.columns = ['date', 'value']

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(df_count_daily['date'], df_count_daily['value'], width=0.8)
for bar in bars:
    height = bar.get_height()
    value = f'{format_number(height)}'
    ax.text(bar.get_x() + bar.get_width() / 2,
            height, value, ha='center', va='bottom')

plt.title('Tổng số giao dịch theo từng ngày')
plt.xticks(rotation=90)
plt.ylabel('Tổng số giao dịch')
plt.ylim(bottom=0.1)
plt.savefig(f'{directory}/daily_count.png')

df_avg_daily = df.groupby(df['issue_date'])['amount'].mean().reset_index()
df_avg_daily.columns = ['date', 'value']

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(df_avg_daily['date'], df_avg_daily['value'], width=0.8)
for bar in bars:
    height = bar.get_height()
    value = f'{format_number(height)}'
    ax.text(bar.get_x() + bar.get_width() / 2,
            height, value, ha='center', va='bottom')

plt.title('Trung bình giao dịch theo từng ngày')
plt.xticks(rotation=90)
plt.ylabel('Trung bình')
plt.ylim(bottom=0.1)
plt.savefig(f'{directory}/daily_avg.png')

df_min_max_daily = df.groupby(df['issue_date'])[
    'amount'].agg(['min', 'max']).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.5
r1 = range(len(df_min_max_daily))
r2 = [x + bar_width for x in r1]
bars1 = ax.bar(r1, df_min_max_daily['min'], color='b',
               width=bar_width, edgecolor='grey', label='Min Value')
bars2 = ax.bar(r2, df_min_max_daily['max'], color='r',
               width=bar_width, edgecolor='grey', label='Max Value')
for bar in bars1:
    height = bar.get_height()
    value = f'{format_number(height)}'
    ax.text(bar.get_x() + bar.get_width() / 2,
            height, value, ha='center', va='bottom', fontsize=6)
for bar in bars2:
    height = bar.get_height()
    value = f'{format_number(height)}'
    ax.text(bar.get_x() + bar.get_width() / 2,
            height, value, ha='center', va='bottom', fontsize=6)

plt.title('Lớn/nhỏ nhất từng ngày')
plt.xticks([r + bar_width / 2 for r in range(len(df_min_max_daily))],
           df_min_max_daily['issue_date'], rotation=90)
plt.legend()
plt.ylabel('Lớn/nhỏ nhất')
plt.ylim(bottom=0.1)
plt.savefig(f'{directory}/daily_min_max.png')
