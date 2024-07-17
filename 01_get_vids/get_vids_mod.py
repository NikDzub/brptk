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
    with open("./etc/users.txt") as f:
        username_list = []
        for line in f.readlines():
            username_list.append(line.replace("\n", ""))
        random.shuffle(username_list)

        top_users = []
        with open("./etc/users_top.txt") as f:
            for line in f.readlines():
                top_users.append(line.replace("\n", ""))
        random.shuffle(top_users)

        top_users = top_users[:5]
        for top in top_users:
            username_list.insert(0, top)
        return split_list(username_list, segments)


def get_used_vids():
    with open("./etc/videos_used.txt", "r") as file:
        used_vids = []
        lines = file.readlines()
        for line in lines:
            used_vids.append(line.replace("\n", ""))
        return used_vids


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
            and (self.hr_ago < 24)
            # and (self.comments > 90)
            and (self.comments < 2000)
        ):
            return True
