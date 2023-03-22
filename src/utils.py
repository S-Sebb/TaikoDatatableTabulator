# -*- coding: utf-8 -*-
import gzip
import json
import os
from pathlib import Path

src_path = Path(os.path.dirname(os.path.realpath(__file__)))
root_path = src_path.parent.absolute()
input_path = os.path.join(root_path, "inputs")
output_musicinfo_table_filepath = os.path.join(root_path, "musicinfo.csv")
output_music_order_table_filepath = os.path.join(root_path, "music_order.csv")
music_attribute_filename = "music_attribute.bin"
music_order_filename = "music_order.bin"
musicinfo_filename = "musicinfo.bin"
wordlist_filename = "wordlist.bin"
datatable_filenames = [music_attribute_filename, music_order_filename, musicinfo_filename, wordlist_filename]
input_datatable_filepaths = [os.path.join(input_path, filename) for filename in datatable_filenames]


def get_datatable_files() -> list:
    data_list = []
    for filepath in input_datatable_filepaths:
        try:
            with open(filepath, "rb") as f:
                json_data = json.loads(gzip.decompress(f.read()).decode("utf-8"))["items"]
            data_list.append(json_data)
        except Exception as e:
            print("Error found in %s" % filepath)
            print(e)
            exit()
    return data_list


def find_cur_dir() -> str:
    return os.getcwd()


def make_dir(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


def enumerate_files(path: str) -> tuple[list, list]:
    output_filepaths = []
    output_filenames = []
    for root, folder, filenames in os.walk(path):
        for filename in filenames:
            output_filepaths.append(os.path.join(root, filename))
            output_filenames.append(filename)
    return output_filepaths, output_filenames


def init() -> None:
    for path in [input_path]:
        make_dir(path)
    for filepath in input_datatable_filepaths:
        if not os.path.exists(filepath):
            print("%s" % filepath + " not found.\n")
            input("Press Enter to exit...")
            exit()
