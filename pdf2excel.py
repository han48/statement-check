import tabula
import PyPDF2
import os

directory = 'output/vcb'
input = 'input/data.pdf'
if not os.path.exists(directory):
    os.makedirs(directory)

total_pages = 0
with open(input, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    total_pages = len(reader.pages)

for page in range(1, total_pages):
    print(f"Export start: {page}/{total_pages - 1}")
    df = tabula.read_pdf(input, pages=page, stream=True)[0]
    df.to_excel(
        f"{directory}/data_{str(page).zfill(8)}.xlsx", index=False)
    print(f"Export   end: {page}/{total_pages - 1}")
