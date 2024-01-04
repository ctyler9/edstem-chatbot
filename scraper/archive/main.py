# import torch
from utils import *
from pprint import pprint


class DataLoader:
    def __init__(self, file_path):
        self.data = read_file(file_path)
        self.delimeter = " ---- "

    def experiment(self):
        # 1672
        thread = self.data[945]
        pprint(thread)

        print(self._parse_thread(thread))
        # if not self._valid_thread(thread):
        #     return None

    def _valid_thread(self, thread):
        # TODO: check if private or not
        response = len(thread.get("children").get("threads")) != 0
        print(response)

        return response

    def _parse_thread(self, thread):
        input_data = thread["subject"] + self.delimeter + thread["content"]
        output_data = [
            content
            for content in thread["children"]["threads"]
            if content != None or content != ""
        ]

        return input_data, output_data
