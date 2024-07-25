from typing import Optional
import textract
import docx2txt

from pdf2docx import Converter
from argparse import ArgumentParser

from spire.doc import *
from spire.doc.common import *


def main():
    parser = ArgumentParser(description="""\
Convert .docx, .pdf, .doc, .xlsx, .xls files in the input folder to text files,
and save in the text_output folder.
""")
    parser.add_argument('-i', '--inputfolder', required=True,
                        help='The folder holds the source files to convert (required)')
    parser.add_argument('-o', '--outputfolder', required=True,
                        help='The folder holds the converted text files (required)')

    args = parser.parse_args()
    input_base_folder = args.inputfolder
    text_base_folder = args.outputfolder

    convert_to_text(input_base_folder, text_base_folder)
    print("done with convert")


def convert_pdf_to_docx(path, raw_file_name):
    cv = Converter(path)
    cv.convert(path+'.docx', start=0, end=None)
    cv.close()
    return raw_file_name+'.docx'


def save_text(text, out_file):
    with open(out_file, 'w', encoding='utf-8') as output:
        output.write(text)


def save_bytes(bytes, out_file):
    with open(out_file, 'wb') as output:
        output.write(bytes)


def textract_text(in_file, out_file):
    text = textract.process(in_file)
    # Write the extracted text to a text file
    save_bytes(text, out_file)


def docx_to_text(in_file, out_file):
    text = docx2txt.process(in_file)
    # Write the extracted text to a text file
    save_text(text, out_file)


def document_to_text(in_file, out_file):
    # Create a Document object
    document = Document()
    # Load a Word document
    document.LoadFromFile(in_file)

    # Extract the text of the document
    document_text = document.GetText()

    # Write the extracted text into a text file
    save_text(document_text, out_file)

    document.Close()


def extract_text(in_file, out_file):
    if in_file.endswith(".docx") or in_file.endswith(".doc"):
        document_to_text(in_file, out_file)


def convert_to_text(in_dir, out_dir):
    # iterate over files in that directory
    for filename in os.listdir(in_dir):
        f = os.path.join(in_dir, filename)
        # checking if it is a file
        if os.path.isfile(f):
            # convert pdf file to docx first, then doing the text conversion
            if f.endswith(".pdf"):
                filename = convert_pdf_to_docx(f, filename)
                f = os.path.join(in_dir, filename)
            # create an text_output file name
            txt_file_name = os.path.join(out_dir, filename + ".txt")
            extract_text(f, txt_file_name)


if __name__ == '__main__':
    main()





