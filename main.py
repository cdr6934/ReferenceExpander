#!/usr/bin/python

import os, sys, getopt
import requests
import re
import markdown
import csv
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('ESV_API_KEY')
API_URL = 'https://api.esv.org/v3/passage/text/'


def get_esv_text(passage):
    params = {
        'q': passage,
        'include-headings': False,
        'include-footnotes': False,
        'include-verse-numbers': False,
        'include-short-copyright': False,
        'include-passage-references': False
    }

    headers = {'Authorization': 'Token %s' % API_KEY}
    response = requests.get(API_URL, params=params, headers=headers)
    passages = response.json()['passages']
    return passages[0].strip() if passages else 'Error: Passage not found'


"""
Creates a csv of all of the scriptures that were in the written document. 
"""


def create_csv(lines):
    with open('verse_output.csv', 'w') as f:
        writer = csv.writer(f)
        for line in lines:
            writer.writerow(line)


def import_file(file_path):
    # TODO add read in try catch
    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()
    return lines


def create_markdown(lines, passages):
    md_file = ""
    for index, line in enumerate(lines, 1):
        md_file += "{0}".format(line)
        for passage in passages:
            if passage[0] == index:
                md_file += "\n> {0} - ({1})\n\n".format(passage[2], str(passage[1]))
    return md_file


def save_markdown(md_file):
    with open('test_file_output.md', 'w') as f:
        for line in md_file:
            f.write(line)


def extract_passages(text):
    results = []
    re_patt = "(?:\d|I{1,3})?\s?\w{2,}\.?\s*\d{1,}\:\d{1,}-?,?\d{0,2}(?:,\d{0,2}){0,2}"
    for index, l in enumerate(text, 1):
        # TODO: Refine REGEX to work for many more
        res = re.findall(re_patt, l)
        if (len(res) > 0):
            for rez in res:
                result = get_esv_text(rez)
                results.append([index, rez, result])
    return results


def main(argv):
    lns = import_file("test_file.md")
    passages = extract_passages(lns)
    res = create_markdown(lns, passages)
    save_markdown(res)
    create_csv(passages)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])
