#!/usr/bin/env python3
import random
import os
import shutil


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


def get_users():
    with open("./etc/user_list.txt") as f:
        username_list = []

        for line in f.readlines():
            username_list.append(line.replace("\n", ""))
        random.shuffle(username_list)

        # top_users = []
        # with open("../etc/top_users.txt") as f:
        #     for line in f.readlines():
        #         top_users.append(line.replace("\n", ""))
        # random.shuffle(top_users)

        # top_users = top_users[:5]
        # for top in top_users:
        #     username_list.insert(0, top)

        return username_list
