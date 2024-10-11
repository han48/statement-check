import pandas as pd
import glob
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from openpyxl import load_workbook

load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
table = "statement_checks"

# Database configuration
db_config = {
    'host': DB_HOST,
    'user': DB_USERNAME,
    'password': DB_PASSWORD,
    'database': DB_DATABASE
}
engine = create_engine(
    f"mysql+mysqlconnector://{DB_USERNAME}:{quote_plus(DB_PASSWORD)}@{DB_HOST}/{DB_DATABASE}")
date_format = "%d/%m/%Y %H:%M:%S"

directory = 'output/standardize'
fileOutput = 'output/vcb.csv'
data = list()

rowCount = 0
datetimeIndex = 1
amountIndex = 2
messageIndex = 3
files = sorted(glob.glob(os.path.join(directory, "*.xlsx")))
data = list()
index = 0

for filename in files:
    workbook = load_workbook(filename)
    sheet = workbook.active
    max_row = sheet.max_row
    for row in range(1, max_row + 1):
        index = index + 1
        amount = str(sheet.cell(row=row, column=amountIndex).value)
        issue_date = str(sheet.cell(row=row, column=datetimeIndex).value)
        message = str(sheet.cell(row=row, column=messageIndex).value)
        data.append([index, issue_date, int(amount), message])
        print(f"[{index}] {filename}")
df = pd.DataFrame(data, columns=['id', 'issue_date', 'amount', 'message'])
print(f"Save to excel: {fileOutput}")
print(f"Import to database: {DB_HOST}:{DB_DATABASE}")
chunk_size = 1000
total_chunks = len(df) // chunk_size + 1
with open(fileOutput, 'w') as writer:
    for i, chunk in enumerate(range(0, len(df), chunk_size)):
        if (i == 0):
            action = 'replace'
            header = True
        else:
            action = 'append'
            header = False
        df_chunk = df.iloc[chunk:chunk + chunk_size]
        startrow = i * chunk_size
        df_chunk.to_csv(writer, header=header, index=False)
        df_chunk.to_sql(table, con=engine, if_exists=action,
                        index=False, method='multi')
        print(f'[{i + 1}/{total_chunks}] ({(i + 1) / total_chunks * 100:.2f}%)')
