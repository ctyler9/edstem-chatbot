import json
import os
import time
import re
import argparse

from piazza_api import Piazza

from utils import *


class PiazzaScraper:
    def __init__(self, login_config_path: str, class_id: str, output_dir_path: str):
        config_params = read_config(login_config_path)
        self.username = config_params["username"]
        self.password = config_params["password"]
        self.class_id = class_id
        self.output_dir = output_dir_path

        self.p = Piazza()
        self.p.user_login(self.username, self.password)

        self.course = self.p.network(self.class_id)
        self.save_dir = os.path.join(self.output_dir, self.class_id, "raw_data")
        create_dir(self.save_dir)

    def get_posts(self):
        self.posts_save_file = os.path.join(self.save_dir, "posts.json")
        master_json = []
        for iter, post in enumerate(self.course.iter_all_posts()):
            master_json.append(post)

            # throttling for API
            self._api_throttling(iter)

        with open(self.posts_save_file, "w") as fp:
            json.dump(master_json, fp)

    def get_users(self):
        users_save_file = os.path.join(self.save_dir, "users.json")
        users = self.course.get_all_users()
        with open(users_save_file, "w") as fp:
            json.dump(users, fp)

    def get_stats(self):
        stats = self.course.get_statistics()
        stats_save_file = os.path.join(self.save_dir, "stats.json")

        with open(stats_save_file, "w") as fp:
            json.dump(stats, fp)

    def _api_throttling(self, iter, verbose=True):
        # rate limited at 60/min
        if verbose:
            print(iter)
        time.sleep(1.1)


class PiazzaParser:
    def __init__(self, output_dir: str, raw_data_posts_path: str):
        # really sloppy
        self.output_dir = output_dir.replace("raw_data", "cleaned_data")
        self.raw_data_json = read_file(raw_data_posts_path)

        create_dir(self.output_dir)

    def write_file(self):
        master_json = self._iterate_through_file()

        with open(
            os.path.join(self.output_dir, "cleaned.json"),
            "w",
        ) as fp:
            json.dump(master_json, fp)

    def _iterate_through_file(self):
        master_json = []
        for thread_idx in range(len(self.raw_data_json)):
            master_json.append(self._read_thread(thread_idx))

        return master_json

    def _read_thread(self, iter):
        thread_dict = {}
        header = self.raw_data_json[iter]["history"][0]
        subject, content = self._pull_parent(header)

        thread_dict["subject"] = subject
        thread_dict["content"] = content

        replies = self.raw_data_json[iter]["children"]
        master_child_list = []
        for reply in replies:
            master_child_list.append(self._pull_children(reply))

        thread_dict["children"] = {"threads": master_child_list}

        return thread_dict

    def _pull_parent(self, payload):
        subject = "subject" in payload.keys()
        content = "content" in payload.keys()

        subject_text = ""
        content_text = ""
        if subject:
            subject_text = payload["subject"]
        if content:
            content_text = payload["content"]

        # clean
        subject_text = self._string_cleaner(subject_text)
        content_text = self._string_cleaner(content_text)

        return subject_text, content_text

    def _pull_children(self, payload):
        children = payload["children"]
        if not payload.get("subject"):
            return None
        if len(children) == 0:
            return self._string_cleaner(payload["subject"])
        else:
            child_list = []
            child_list.append(self._string_cleaner(payload["subject"]))
            for child in children:
                child_list.append(self._pull_children(child))

            return {"content": child_list}

    def _string_cleaner(self, text: str):
        rx = re.compile(r"<.*?>|\\.*?\\|\n|\xa0|&.*?;")
        res = rx.sub("", text).strip()

        return res


def main():
    parser = argparse.ArgumentParser(description="Piazza Scraper and Parser")
    parser.add_argument(
        "--login_config_path",
        type=str,
        help="path to your config file with username and pass for piazza",
    )
    parser.add_argument("--class_id", type=str, help="Class ID for piazza thread")

    parser.add_argument(
        "--output_dir_path", type=str, help="Where you want to output your files"
    )

    args = parser.parse_args()

    login_config_path = args.login_config_path
    class_id = args.class_id
    output_dir_path = args.output_dir_path

    ps = PiazzaScraper(login_config_path, class_id, output_dir_path)

    ps.get_posts()
    ps.get_users()
    ps.get_stats()

    raw_data_posts_path = ps.posts_save_file
    save_dir = ps.save_dir

    pp = PiazzaParser(save_dir, raw_data_posts_path)

    pp.write_file()


if __name__ == "__main__":
    main()
