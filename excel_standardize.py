import glob
import os

from pdf_helpers import standardize_excel_plumber, standardize_excel_tabula, standardize_excel_tabula2

directory = 'output/vcb'

files = sorted(glob.glob(os.path.join(directory, "data_0???????.xlsx")))
for filename in files:
    fileOutput = filename.replace('vcb', 'standardize')
    standardize_excel_tabula(filename, fileOutput)

files = sorted(glob.glob(os.path.join(directory, "data_1???????.xlsx")))
for filename in files:
    fileOutput = filename.replace('vcb', 'standardize')
    standardize_excel_plumber(filename, fileOutput)

files = sorted(glob.glob(os.path.join(directory, "data_2???????.xlsx")))
for filename in files:
    fileOutput = filename.replace('vcb', 'standardize')
    standardize_excel_plumber(filename, fileOutput)

files = sorted(glob.glob(os.path.join(directory, "data_3???????.xlsx")))
for filename in files:
    fileOutput = filename.replace('vcb', 'standardize')
    standardize_excel_plumber(filename, fileOutput)

files = sorted(glob.glob(os.path.join(directory, "data_4???????.xlsx")))
for filename in files:
    fileOutput = filename.replace('vcb', 'standardize')
    standardize_excel_plumber(filename, fileOutput)

files = sorted(glob.glob(os.path.join(directory, "data_5???????.xlsx")))
for filename in files:
    fileOutput = filename.replace('vcb', 'standardize')
    standardize_excel_plumber(filename, fileOutput)

files = sorted(glob.glob(os.path.join(directory, "data_6???????.xlsx")))
for filename in files:
    fileOutput = filename.replace('vcb', 'standardize')
    standardize_excel_tabula2(filename, fileOutput)

files = sorted(glob.glob(os.path.join(directory, "data_7???????.xlsx")))
for filename in files:
    fileOutput = filename.replace('vcb', 'standardize')
    standardize_excel_tabula2(filename, fileOutput)

files = sorted(glob.glob(os.path.join(directory, "data_8???????.xlsx")))
for filename in files:
    fileOutput = filename.replace('vcb', 'standardize')
    standardize_excel_tabula2(filename, fileOutput)

files = sorted(glob.glob(os.path.join(directory, "data_9???????.xlsx")))
for filename in files:
    fileOutput = filename.replace('vcb', 'standardize')
    standardize_excel_tabula2(filename, fileOutput)

files = sorted(glob.glob(os.path.join(directory, "data_10???????.xlsx")))
for filename in files:
    fileOutput = filename.replace('vcb', 'standardize')
    standardize_excel_tabula2(filename, fileOutput)