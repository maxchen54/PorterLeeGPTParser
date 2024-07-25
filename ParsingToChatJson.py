
import os
import json
import re
from argparse import ArgumentParser

def save_text(text, out_file):
    with open(out_file, 'w') as output:
        output.write(text)


def save_bytes(bytes, out_file):
    with open(out_file, 'wb') as output:
        output.write(bytes)


def final_json_conversion(parsing_metadata, is_new_format):
    with open(parsing_metadata.text_file_path, "r", encoding="utf-8") as text_input:
        has_previous = False
        saved_block = ""
        output = ""
        while True:
            line = text_input.readline()
            # if found closing pattern or line is empty
            # end of file is reached
            if is_pattern_match(line, parsing_metadata.closing_pattern) or not line:
                break

            # ignore the line with only a new line character
            #if not line.strip():
            #    continue

            if is_pattern_match(line, parsing_metadata.ignore_pattern):
                print("Discard : " + line)
                continue

            if is_pattern_match(line, parsing_metadata.starting_pattern):
                print("got one line")
                if has_previous is True:
                    # we need to flush the previous saved block to json text_output
                    output = concat_json_output(saved_block, output, parsing_metadata.split_pattern, is_new_format)

                else:
                    has_previous = True

                # always save this line to be the first one in saved_block
                saved_block = line
            elif has_previous is True:
                # concat this line
                saved_block += line
            else:
                print("Ignore : " + line)

        # process the last saved block
        output = concat_json_output(saved_block, output, parsing_metadata.split_pattern, is_new_format)

    save_text(output, parsing_metadata.json_file_path)


def is_pattern_match(line, pattern):
    if pattern is None:
        return False
    result = re.match(pattern, line, re.IGNORECASE)
    if result:
        return True
    return False


def concat_json_output(saved_block, json_to_concat, pattern, is_new_format):
    json_out_local = flush_block(saved_block, pattern, is_new_format)
    # find a valid json text_output
    if json_out_local is not None:
        json_to_concat += json_out_local + "\n"
    return json_to_concat


def flush_block(saved_block, pattern, is_new_format):
    parser = BlockParser(pattern, is_new_format)
    return parser.get_json_output(saved_block)


# Merge the datasets into a single file
def merge_datasets(in_dir, output_file):
    with open(output_file, 'w') as outfile:
        for filename in os.listdir(in_dir):
            fname = os.path.join(in_dir, filename)
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

class BlockParser:

    def __init__(self, pattern, is_new_format):
        self.pattern = pattern
        self.is_new_format = is_new_format

    def get_json_output(self, text_block):
        result_list = re.split(self.pattern, text_block, 1)
        if len(result_list) != 2:
            return None

        response = result_list[1].strip()
        if len(response) == 0:
            return None

        if self.is_new_format:
            one_piece = BlockParser.to_chat_format(result_list[0].strip(), response)
        else:
            one_piece = BlockParser.to_pair_format(result_list[0].strip(), response)

        json_out = json.dumps(one_piece)
        print(json_out)
        return json_out

    @staticmethod
    def to_pair_format(prompt, response):
        # used for tuning old model, like davinci-002
        return {"prompt": prompt, "completion": response}

    @staticmethod
    def to_chat_format(prompt, response):
        # used for tuning gpt gpt-3.5-turbo model
        system = {"role": "system", "content": "A chat bot for RFP"}
        user = {"role": "user", "content": prompt}
        assistant = {"role": "assistant", "content": response}
        return {"messages": [system, user, assistant]}

class ParsingMetadata:

    def __init__(self, file_name, starting_pattern, split_pattern, ignore_pattern, closing_pattern):
        self.starting_pattern = starting_pattern
        self.split_pattern = split_pattern
        self.ignore_pattern = ignore_pattern
        self.closing_pattern = closing_pattern
        self.text_file_path = os.path.join(text_base_folder, file_name)
        self.json_file_path = os.path.join(json_base_folder, file_name + ".jsonl")


if __name__ == '__main__':
    parser = ArgumentParser(description="""\
    Convert .txt files in the input folder to .jsonl files, saved into the output folder. 
    Merge the .jsonl files into one large .jsonl database file for fine-tuning.
    """)
    parser.add_argument('-i', '--inputfolder', required=True,
                        help='The folder that holds the .txt files to convert (required)')
    parser.add_argument('-o', '--outputfolder', required=True,
                        help='The folder that holds the converted .jsonl format files (required)')
    parser.add_argument('-j', '--jsondataset', required=True,
                        help='A merged .jsonl file containing data from each individual .jsonl file (required)')

    args = parser.parse_args()
    text_base_folder = args.inputfolder # text_output
    json_base_folder = args.outputfolder # json_output
    json_merged_dataset = args.jsondataset #merged_dataset file

    file_name_1 = "4_TechRequirements.docx.txt"
    starting_pattern = ('^.*((system shall)|(system should)|(vendor shall)|'
                        '(vendor should)|(system must)|(Per ISO/IEC)).*$')
    split_pattern = '\n'
    ignore_pattern = "^[A-Z][.].+$"

    metadata1 = ParsingMetadata(file_name_1, starting_pattern, split_pattern, ignore_pattern, None)
    final_json_conversion(metadata1, True)
    print("done with json out")

    file_name_2 = "C_Tech & Funct RequirmentsTable.docx.txt"
    # one of more uppercase letter followed by a space followed by one or more digits followed by dot
    starting_pattern = '^[A-Z]+\\s[0-9]+[.].+$'
    split_pattern = 'F\n|T\n|NV\n|M\n'
    ignore_pattern = "^(Yes)|(CR)|(EX)|(DR).*$"
    closing_pattern = "^(Screen Shot Appendix For Functional Requirements Table\n)$"

    metadata2 = ParsingMetadata(file_name_2, starting_pattern, split_pattern, ignore_pattern, closing_pattern)
    final_json_conversion(metadata2, True)
    print("done with json out")

    file_name_3 = "JUS-RFP24-0224GW_Q_A_Response.pdf.docx.txt"
    starting_pattern = '^[\\s\t]*[0-9]+[.].+$'
    split_pattern = '\n'
    ignore_pattern = "^.*(Technical Questions:).*$"

    metadata3 = ParsingMetadata(file_name_3, starting_pattern, split_pattern, ignore_pattern, None)
    final_json_conversion(metadata3, True)
    print("done with json out")

    file_name_4 = "Section 3 - LIMS Requirements and Deliverables Checklist.docx.txt"
    starting_pattern = '^[0-9]+[.][0-9]+(([.][0-9]+)|(\\s)).*$'
    split_pattern = 'Explanation:\\s'
    ignore_pattern = '^((Scoring Criteria)|X)\n$'

    metadata4 = ParsingMetadata(file_name_4, starting_pattern, split_pattern, ignore_pattern, None)
    final_json_conversion(metadata4, True)
    print("done with json out")

    merge_datasets(json_base_folder, json_merged_dataset)
    print("Merged dataset")