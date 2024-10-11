import glob
import os
import sys
import pdfplumber

from pdf_helpers import process_pdf_plumber

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
    if argv_len >= 4:
        reverse = "1" == sys.argv[3] or "True" == sys.argv[3]
    else:
        reverse = False

    if not os.path.exists(directory):
        os.makedirs(directory)

    sum_pages = 0
    current_pages = 0
    total_files = 1

    with pdfplumber.open(input) as pdf:
        sum_pages = sum_pages + len(pdf.pages)
        total_pages = len(pdf.pages)
        if (reverse):
            ranges = reversed(range(1, total_pages))
        else:
            ranges = range(1, total_pages)
        for page in ranges:
            current_pages = current_pages + 1
            process_pdf_plumber(
                [pdf, page, total_pages, prefix, directory],
                [total_files, sum_pages, current_pages]
            )
    prefix = prefix + 1
    exit(1)
