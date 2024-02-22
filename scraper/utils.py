import json
import os

def read_config(file_path):
    with open(file_path) as fp:
        dump = json.load(fp)

    return dump


def read_file(file_path):
    with open(file_path) as fp:
        data = json.load(fp)

    return data


def create_dir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)
