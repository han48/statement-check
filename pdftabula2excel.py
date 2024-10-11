import glob
import PyPDF2
import sys
import os

from pdf_helpers import process_pdf_tabula


if __name__ == "__main__":
    directory = os.getenv('OUTPUT')
    inputDirectory = os.getenv('INPUT')
    argv_len = len(sys.argv)
    if argv_len >= 2:
        input = sys.argv[1]
    else:
        input = sorted(glob.glob(os.path.join(inputDirectory, "*.pdf")))[0]
    if argv_len >= 3:
        prefix = sys.argv[2]
    else:
        prefix = 0
    if not os.path.exists(directory):
        os.makedirs(directory)

    total_pages = 0
    with open(input, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)

    start_page = 1
    for page in range(start_page, total_pages):
        process_pdf_tabula([input, page, total_pages, prefix, directory])
