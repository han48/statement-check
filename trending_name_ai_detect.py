import pandas as pd
import csv
import os
from pdf_helpers import ai_extract_fullname
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline


directory = 'output/chart/vcb'
if not os.path.exists(directory):
    os.makedirs(directory)

fileOutput = 'output/vcb.csv'
df = pd.read_csv(fileOutput)
full_names = list()

index = 1
total = len(df['message'])
cache_dir = '__cache__'
model_name = 'undertheseanlp/vietnamese-ner-v1.4.0a2'
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
model = AutoModelForTokenClassification.from_pretrained(
    model_name, num_labels=9, cache_dir=cache_dir)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, device=0)
directory_name = 'output/name/vcb'
if not os.path.exists(directory_name):
    os.makedirs(directory_name)
filename = directory_name + '/full_names.csv'
file_exists = os.path.isfile(filename)
start_index = 1
if start_index == 1:
    mode = 'w'
else:
    mode = 'a'
with open(filename, mode=mode, newline='') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(['Name'])  # Adjust the header as needed
    for index in range(start_index, total):
        message = df['message'][index]
        message = str(message).lower()
        full_name = ai_extract_fullname(message, ner_pipeline)
        if len(full_name) > 0:
            if len(full_name) == 1:
                writer.writerows([full_name])
            else:
                writer.writerows(full_name)
        print(f"[{index}/{total}]")
