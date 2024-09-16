import pandas as pd
import glob
import os
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import create_engine
from urllib.parse import quote_plus

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

directory = 'output/vcb'
data = list()

rowCount = 0
datetimeIndex = 0
amountIndex = 2
messageIndex = 4
files = sorted(glob.glob(os.path.join(directory, "*.xlsx")))

for filename in files:
    df = pd.read_excel(filename)
    total_rows = df.shape[0]
    index = 0
    print(f"============={filename}=============")
    while (index <= total_rows - 1):
        row = df.iloc[index]
        amount = str(row.iloc[amountIndex]).replace(".", "")
        if (amount.isnumeric()):
            issue_date = datetime.strptime(str(
                df.iloc[index - 1].iloc[datetimeIndex]) + " 00:00:00", date_format).strftime('%Y-%m-%d %H:%M:%S')
            message = str(row.iloc[messageIndex])
            data.append([rowCount, issue_date, int(amount), message])
            rowCount = rowCount + 1
        elif (len(data) > 0):
            message = str(row.iloc[messageIndex])
            if (message != "nan"):
                data[len(data) - 1][3] = data[len(data) - 1][3] + \
                    " " + message
        index = index + 1

df = pd.DataFrame(data, columns=['id', 'issue_date', 'amount', 'message'])
df.to_sql(table, con=engine, if_exists='replace', index=False)
