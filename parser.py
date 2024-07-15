import json
import os
import textract
import pdf2docx
import re


def file_to_txt(filename, file_dir):
    if ".pdf" in filename:
        print("pdf convert")
        filename = pdf_to_docx(filename, file_dir)
    full_path = os.path.join(file_dir, filename)
    txt_output = textract.process(full_path)
    return txt_output


def pdf_to_docx(filename, file_dir):
    pdf2docx.parse(str(os.path.join(file_dir, filename)))

    return filename


def save(dest, text):
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(text.decode("utf-8"))


def convert(file_dir):
    for file_name in os.listdir(file_dir):
        text = file_to_txt(file_name, file_dir)
        output_file_path = "output/" + file_name + ".txt"
        save(output_file_path, text)


def parse_block(block, metadata):
    parts = re.split(metadata.split_block, block, maxsplit=1)
    if len(parts) != 2:
        return False
    if len(parts[1]) == 0:
        return False
    parts[0] = parts[0].strip()
    parts[1] = parts[1].strip()
    single_pair = {'Prompt': parts[0], 'Completion': parts[1]}
    json_pair = json.dumps(single_pair)
    return json_pair


def parse_file(metadata):
    with open(metadata.file_path, 'r', encoding='utf-8') as f:
        line = f.readline()
        is_first_block = True
        last_block = ""
        json_output = []

        while True:
            if not line:
                print("end of file")
                break

            if re.match(metadata.start_block, line):
                if is_first_block:
                    is_first_block = False
                    continue
                else:
                    json_pair = parse_block(last_block, metadata)
                    if json_pair:
                        json_output.append(json_pair)
                    last_block = ""

            last_block += line
            line = f.readline()

        print(json_output)


class ParsingMetadata:
    def __init__(self, start_block, split_block, end_block, file_path):
        self.start_block = start_block
        self.split_block = split_block
        self.end_block = end_block
        self.file_path = file_path


if __name__ == "__main__":
    file_directory = "data/"
    output_directory = "output/"
    convert(file_directory)
    file_metadata_1 = ParsingMetadata(r'\d+\.\d+\.\d',
                                      r'\n+[A-Z0-9]\n+',
                                      None,
                                      file_path=os.path.join(output_directory,
                                                             "Section 3 - LIMS Requirements and Deliverables "
                                                             "Checklist.docx.txt"))
    file_metadata_2 = ParsingMetadata(r'(shall|The system must|Per ISO/IEC|The system should)',
                                      r'\n',
                                      None,
                                      file_path=os.path.join(output_directory,
                                                             "4_TechRequirements.docx.txt"))
    file_metadata_3 = ParsingMetadata(r'')

    parse_file(file_metadata_1)
    parse_file(file_metadata_2)

# save each file as metadata and determine which parser to use, make multiple parsers that go off of
# newlines, "the system shall", etc.
