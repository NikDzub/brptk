#!/usr/bin/env python3
import random
import os
import shutil


url = "https://www.tiktok.com/"


def split_list(li, segments):
    segment_size = len(li) // segments
    remainder = len(li) % segments
    segments_list = []
    start = 0
    for i in range(segments):
        if i < remainder:
            end = start + segment_size + 1
        else:
            end = start + segment_size
        segments_list.append(li[start:end])
        start = end
    return segments_list


def get_users(segments):
    with open("./01_get_vids_loop/etc/users.txt") as f:
        username_list = []
        for line in f.readlines():
            username_list.append(line.replace("\n", ""))
        random.shuffle(username_list)
        username_list = username_list[:20]

        top_users = []
        with open("./01_get_vids_loop/etc/users_top.txt") as f:
            for line in f.readlines():
                top_users.append(line.replace("\n", ""))
        random.shuffle(top_users)

        top_users = top_users[:2]
        for top in top_users:
            username_list.insert(0, top)
        return split_list(username_list, segments)


def get_all_users():
    with open("./01_get_vids_loop/etc/users.txt") as f:
        username_list = []
        for line in f.readlines():
            username_list.append(line.replace("\n", ""))
        random.shuffle(username_list)

        top_users = []
        with open("./01_get_vids_loop/etc/users_top.txt") as f:
            for line in f.readlines():
                top_users.append(line.replace("\n", ""))
        random.shuffle(top_users)
        for top in top_users:
            username_list.insert(0, top)
        return username_list


def get_used_vids():
    with open("./01_get_vids_loop/etc/videos_used.txt", "r") as file:
        used_vids = []
        lines = file.readlines()
        for line in lines:
            used_vids.append(line.replace("\n", ""))
        return used_vids


def get_new_vids():
    with open("./01_get_vids_loop/etc/videos_new.txt", "r") as file:
        new_vids = []
        lines = file.readlines()
        for line in lines:
            new_vids.append(line.replace("\n", ""))
        return new_vids


def update_new_vids(url_to_remove):
    with open("./01_get_vids_loop/etc/videos_new.txt", "r") as file:
        new_vids = []
        lines = file.readlines()
        for line in lines:
            new_vids.append(line.replace("\n", ""))

    with open("./01_get_vids_loop/etc/videos_new.txt", "w") as file:
        for url in new_vids:
            if url_to_remove != url:
                file.write(url + "\n")

    with open("./01_get_vids_loop/etc/videos_used.txt", "r") as file:
        used_vids = []
        lines = file.readlines()
        for line in lines:
            used_vids.append(line.replace("\n", ""))

        used_vids.append(url_to_remove)

        with open("./01_get_vids_loop/etc/videos_used.txt", "w") as file:
            for used_url in used_vids:
                file.write(used_url + "\n")


def clean_firefox():
    context_dir = "./firefox"
    context_dir = os.path.join(os.getcwd(), context_dir)
    try:
        shutil.rmtree(f"{context_dir}/sessionstore-backups")
        os.remove(f"{context_dir}/sessionCheckpoints.json")
        os.remove(f"{context_dir}/sessionstore.jsonlz4")
    except Exception as error:
        pass
        # print(error)


def clean_local_firefox():
    context_dir = "/Users/ihpt/Library/Application Support/Firefox/Profiles/i8unqabt.default-nightly"
    context_dir = os.path.join(os.getcwd(), context_dir)
    try:
        shutil.rmtree(f"{context_dir}/storage")
        shutil.rmtree(f"{context_dir}/crashes")
        shutil.rmtree(f"{context_dir}/sessionstore-backups")
        os.remove(f"{context_dir}/sessionCheckpoints.json")
        os.remove(f"{context_dir}/sessionstore.jsonlz4")
    except Exception as error:
        pass
        # print(error)


class Video:
    def __init__(
        self,
        creator,
        verified,
        vid_id,
        hr_ago,
        comments,
        likes,
        plays,
        bookmarks,
        shares,
    ):
        self.creator = creator
        self.verified = verified
        self.vid_id = vid_id
        self.hr_ago = hr_ago
        self.comments = comments
        self.likes = likes
        self.plays = plays
        self.bookmarks = bookmarks
        self.shares = shares

    def display_info(self):
        print(
            f"\n{url}@{self.creator}/video/{self.vid_id} \nhr_ago: {int(self.hr_ago)} comments: {self.comments} likes: {self.likes:,} plays: {self.plays:,} bookmarks: {self.bookmarks:,} shares: {self.shares:,}"
        )

    def video_url(self):
        # print(f"{url}@{self.creator}/video/{self.vid_id}")
        return f"{url}@{self.creator}/video/{self.vid_id}"

    def valid(self):
        if (
            (self.likes / (self.hr_ago * 1000) > 0.5)
            and (self.hr_ago < 22)
            and (self.comments > 300)
            and (self.comments < 999999)
        ) or (
            (self.likes / (self.hr_ago * 1000) > 0.5)
            and (self.hr_ago < 1)
            and (self.comments > 150)
            and (self.comments < 999999)
        ):
            return True
