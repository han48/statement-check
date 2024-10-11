import glob
import PyPDF2
import os
from dotenv import load_dotenv

from pdf_helpers import process_pdf_camelot
load_dotenv(override=True)

directory = os.getenv('OUTPUT')
inputDirectory = os.getenv('INPUT')

if not os.path.exists(directory):
    os.makedirs(directory)

files = sorted(glob.glob(os.path.join(inputDirectory, "*.pdf")))

prefix = 0
for input in files:
    total_pages = 0
    with open(input, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)

    for page in range(1, total_pages):
        process_pdf_camelot([input, page, total_pages, prefix, directory])
    prefix = prefix + 1
