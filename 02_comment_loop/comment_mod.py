#!/usr/bin/env python3
import random
import os
import shutil

new_vids_path = "./01_get_vids_loop/etc/videos_new.txt"


def get_new_vids():
    with open(new_vids_path, "r") as file:
        new_vids = []
        lines = file.readlines()
        for line in lines:
            new_vids.append(line.replace("\n", ""))
        return new_vids


def clear_new_vids():
    with open(new_vids_path, "w") as file:
        pass
