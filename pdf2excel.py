import glob
import PyPDF2
import os
from dotenv import load_dotenv
import pdfplumber

from pdf_helpers import process_pdf_camelot, process_pdf_plumber, process_pdf_tabula
load_dotenv(override=True)

directory = os.getenv('OUTPUT')
inputDirectory = os.getenv('INPUT')

if not os.path.exists(directory):
    os.makedirs(directory)

files = sorted(glob.glob(os.path.join(inputDirectory, "*.pdf")))

prefix = 0
inputs = list()
total_pages = 0
total_files = 0
for input in files:
    with pdfplumber.open(input) as pdf:
        print(f"Loading total page: {input}")
        total_page = len(pdf.pages)
        total_pages = total_pages + total_page
        total_files = total_files + 1
        inputs.append((input, total_page))

current_pages = 0
for input, total_page in inputs:
    input_type = str(input).split('.')
    input_type = input_type[len(input_type) - 2]
    ranges = range(1, total_page)
    match input_type:
        case 'tabula':
            for page in ranges:
                try:
                    current_pages = current_pages + 1
                    process_pdf_tabula(
                        [input, page, total_pages, prefix, directory],
                        [total_files, total_pages, current_pages]
                    )
                except Exception as e:
                    print(f"    {str(e)}")
        case 'plumber':
            with pdfplumber.open(input) as pdf:
                for page in ranges:
                    try:
                        current_pages = current_pages + 1
                        process_pdf_plumber(
                            [pdf, page, total_page, prefix, directory],
                            [total_files, total_pages, current_pages]
                        )
                    except Exception as e:
                        print(f"    {str(e)}")
    prefix = prefix + 1
