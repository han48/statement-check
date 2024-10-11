import os
import sys
import glob
import pdfplumber

from pdf_helpers import process_pdf_plumber


if __name__ == "__main__":
    argv_len = len(sys.argv)
    directory = 'output/vcb'
    if argv_len >= 2:
        reverse = "1" == sys.argv[1] or "True" == sys.argv[1]
    else:
        reverse = False

    directory = os.getenv('OUTPUT')
    inputDirectory = os.getenv('INPUT')
    if not os.path.exists(directory):
        os.makedirs(directory)

    files = glob.glob(os.path.join(inputDirectory, "*.pdf"))
    files = sorted(files)

    prefix = 0
    total_files = len(files)

    sum_pages = 0
    current_pages = 0
    for input in files:
        with pdfplumber.open(input) as pdf:
            sum_pages = sum_pages + len(pdf.pages)

    for input in files:
        with pdfplumber.open(input) as pdf:
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
