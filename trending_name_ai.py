from collections import Counter
import matplotlib.pyplot as plt
import re
import os

from pdf_helpers import format_number


def remove_elements(lst, X):
    return [element for element in lst if element != X]


def top_10(lst):
    counter = Counter(lst)
    top_10 = counter.most_common(10)
    return top_10


def replace_numbers_and_special_characters(text):
    return re.sub(r'[^a-zA-Z\s]', '', text)


def clean_name(text):
    text = text.lower()
    text = replace_numbers_and_special_characters(text)
    fullname = text.split()
    fullname = remove_elements(fullname, 'partner')
    fullname = remove_elements(fullname, 'vietcom')
    fullname = remove_elements(fullname, 'vietcomban')
    fullname = remove_elements(fullname, 'ibft')
    fullname = remove_elements(fullname, 'nguy')
    fullname = remove_elements(fullname, 'direct')
    fullname = remove_elements(fullname, 'deb')
    fullname = remove_elements(fullname, 'debits')
    fullname = remove_elements(fullname, 'debitsc')
    fullname = remove_elements(fullname, 'ib')
    if len(fullname) > 0:
        firstname = fullname[0]
    else:
        firstname = None
    if len(fullname) > 1:
        lastname = fullname[len(fullname) - 1]
    else:
        lastname = None
    return [firstname, lastname]


directory = 'output/chart/vcb'
if not os.path.exists(directory):
    os.makedirs(directory)

filename = 'output/name/vcb/full_names.csv'
lst_firstname = list()
lst_lastname = list()
with open(filename, 'r') as file:
    for line in file:
        firstname, lastname = clean_name(line)
        lst_firstname.append(firstname)
        lst_lastname.append(lastname)

lst_firstname = remove_elements(lst_firstname, None)
lst_lastname = remove_elements(lst_lastname, None)
top_firstname = top_10(lst_firstname)
top_lastname = top_10(lst_lastname)

labels, values = zip(*top_firstname)
labels = [label.capitalize() for label in labels]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(labels, values, width=0.8)
for bar in bars:
    height = bar.get_height()
    value = f'{format_number(height)}'
    ax.text(bar.get_x() + bar.get_width() / 2,
            height, value, ha='center', va='bottom')

plt.title('Thống kê theo Họ (sử dụng AI)')
plt.xticks(rotation=90)
plt.ylabel('Tổng hợp giao dịch')
plt.ylim(bottom=0.1)
plt.savefig(f'{directory}/firstname_sum.png')

labels, values = zip(*top_lastname)
labels = [label.capitalize() for label in labels]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(labels, values, width=0.8)
for bar in bars:
    height = bar.get_height()
    value = f'{format_number(height)}'
    ax.text(bar.get_x() + bar.get_width() / 2,
            height, value, ha='center', va='bottom')

plt.title('Thống kê theo Tên (sử dụng AI)')
plt.xticks(rotation=90)
plt.ylabel('Tổng hợp giao dịch')
plt.ylim(bottom=0.1)
plt.savefig(f'{directory}/lastname_sum.png')